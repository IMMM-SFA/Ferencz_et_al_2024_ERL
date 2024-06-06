# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import os 
import geopandas
import rasterio
from rasterio.mask import mask
from rasterio.plot import show

# Path to clipped landcover rasters by water provider footprint and NLCD LC in LA County (Folder MSDLive: Clipped_Provider_High_Res_Landcover) 
os.chdir(Path to clipped landcover rasters)

# find unique water provider service region names
file_names = os.listdir()

regions = []
for i in range(len(file_names)):
    file_name = file_names[i]
    length = len(file_name)
    service_region = file_name[0:length-17]    
    regions.append(service_region)
   
# list of water provider service regions 
regions = np.unique(regions)
regions = regions.tolist()

#%% Clipped Landover and NLCD Land Class (LC) Processing to Calculate Landcover areas and fractions by NLCD landclass for each provider 

# construct dataframe for results 
# rows are service regions, 16 columns of results that are the average green 
# fraction for each NLCD urban landclass (LC21, LC22, LC23, LC24)  
columns = ['LC_21_tree', 'LC_21_grass', 'LC_21_shrub', 'LC_21_dirt_brown_veg', 
           'LC_22_tree', 'LC_22_grass', 'LC_22_shrub', 'LC_22_dirt_brown_veg', 
           'LC_23_tree', 'LC_23_grass', 'LC_23_shrub', 'LC_23_dirt_brown_veg', 
           'LC_24_tree', 'LC_24_grass', 'LC_24_shrub', 'LC_24_dirt_brown_veg'] 

# dataframe for landcover fraction
landcover_fraction = pd.DataFrame(data = np.zeros((len(regions), 16)), index = regions, columns = columns)

# dataframe for Landclass area (LC)
LC_area = pd.DataFrame(data = np.zeros((len(regions), 5)), 
                                  index = regions, 
                                  columns = ['LC_21', 'LC_22', 'LC_23', 'LC_24', 'All_LC'])

raster_suffix = ['_LC_21_hi_res.tif', '_LC_22_hi_res.tif', '_LC_23_hi_res.tif',
                 '_LC_24_hi_res.tif']

# caculate landcover fraction for each service region
for i, cell in enumerate(regions):
    
    # load clipped landcover raster 
    for lc in range(4):
        
        raster_file = cell + raster_suffix[lc]
        
        try:
            with rasterio.open(raster_file, 'r') as ds:
                arr = ds.read()  # read all raster values
        
        except:
            continue 
            
        #show(ds)
        
        area = np.array(arr[0,:,:])
        area_filt = np.where(area < 6, area, np.nan)
        area_filt = area_filt.flatten()
        area_filt = area_filt[~np.isnan(area_filt)]
        
        lc_area = len(area_filt)
        
        LC_area.iloc[i, lc] = lc_area
        
        class_1 = np.where(area_filt == 1, area_filt, np.nan)
        class_1 = class_1[~np.isnan(class_1)]
        class_2 = np.where(area_filt == 2, area_filt, np.nan)
        class_2 = class_2[~np.isnan(class_2)]
        class_3 = np.where(area_filt == 3, area_filt, np.nan)
        class_3 = class_3[~np.isnan(class_3)]
        class_4 = np.where(area_filt == 4, area_filt, np.nan)
        class_4 = class_4[~np.isnan(class_4)]
        
        landcover_fraction.iloc[i, 4*lc] = len(class_1)/lc_area
        landcover_fraction.iloc[i, 4*lc + 1] = len(class_2)/lc_area
        landcover_fraction.iloc[i, 4*lc + 2] = len(class_3)/lc_area
        landcover_fraction.iloc[i, 4*lc + 3] = len(class_4)/lc_area

#%% Additional processing and scatter plots 

# LC data - convert cell counts to area
for i in range(len(regions)):
    for j in range(4):
        LC_area.iloc[i,j] = LC_area.iloc[i,j] * 0.36 # convert to area 0.36 m^2/pixel (60 cm x 60 cm)
        
        if j == 3:
            LC_area.iloc[i,4] = np.sum(LC_area.iloc[i,0:4]) # sum total LC area in region

# Add weighted landclass (LC) field 
LC_area['Weighted_LC'] = np.zeros(len(regions)) # add new column weighted LC 

# Calculate area-weighted landclass 
for i in range(len(regions)):
    LC_area.iloc[i,5] = 21 * (LC_area.iloc[i,0]/LC_area.iloc[i,4]) + \
                            22 * (LC_area.iloc[i,1]/LC_area.iloc[i,4]) + \
                            23 * (LC_area.iloc[i,2]/LC_area.iloc[i,4]) + \
                            24 * (LC_area.iloc[i,3]/LC_area.iloc[i,4]) 

# Convert landcover fraction to landcover areas (m^2) using landclass (LC) areas and
# landcover fraction data 
landcover_area = pd.DataFrame(data = np.zeros((len(regions), 16)), 
                                  index = regions, columns = columns)

for i in range(len(regions)):
    landcover_area.iloc[i,0:4] = landcover_fraction.iloc[i,0:4] * LC_area.iloc[i,0]
    landcover_area.iloc[i,4:8] = landcover_fraction.iloc[i,4:8] * LC_area.iloc[i,1]
    landcover_area.iloc[i,8:12] = landcover_fraction.iloc[i,8:12] * LC_area.iloc[i,2]
    landcover_area.iloc[i,12:] = landcover_fraction.iloc[i,12:] * LC_area.iloc[i,3]


#%% Combine the multi-part tiff files
# Sum rows with multiple parts
# Sum, append, and delete extra rows

multi_part_county = ['CTY_LAX', 'IOU_SGV', 'IOU_SWS_SJH', 'IOU_SWS_WLM'] # change from county to city, or use multi_part_provider

#%%

# Rename Index
Landcover_area = landcover_area.reset_index()
Landcover_area.rename(columns = {'index': 'ARTES_ID'}, inplace = True)

for i in multi_part_county:
    rows_to_delete = Landcover_area['ARTES_ID'].str.startswith(i) 
    rows_to_sum = Landcover_area['ARTES_ID'].str.startswith(i) #
    summed_values = Landcover_area.loc[rows_to_sum, :].sum(axis=0)
    
    # Delete the rows asscoiated with the multi_part_county
    Landcover_area = Landcover_area.drop(Landcover_area[rows_to_delete].index)
    
    # Create a new row with the summed values for the multi_part_county
    new_row = pd.DataFrame([summed_values.values], columns=Landcover_area.columns)
    new_row['ARTES_ID'] = i
    Landcover_area = pd.concat([Landcover_area, new_row], ignore_index=True)

# Rename index
Landcover_area = Landcover_area.set_index('ARTES_ID')

#%%

# Rename index
LC_area = LC_area.reset_index()
LC_area.rename(columns = {'index': 'ARTES_ID'}, inplace = True)


for i in multi_part_county:
    rows_to_delete = LC_area['ARTES_ID'].str.startswith(i)
    rows_to_sum = LC_area['ARTES_ID'].str.startswith(i)
    summed_values = LC_area.loc[rows_to_sum, :].sum(axis=0)

    # Delete the rows asscoiated with the multi_part_county
    LC_area = LC_area.drop(LC_area[rows_to_delete].index)
    
    # Create a new row with the summed values for the multi_part_county
    new_row = pd.DataFrame([summed_values.values], columns=LC_area.columns)
    new_row['ARTES_ID'] = i
    LC_area = pd.concat([LC_area, new_row], ignore_index=True)

# Rename index
LC_area = LC_area.set_index('ARTES_ID') # check Weighted LC for LC_area

#%%
Landcover_fraction = landcover_fraction.copy()

for i in multi_part_county:
    # Delete old rows
    Landcover_fraction = Landcover_fraction[~Landcover_fraction.index.str.startswith(i)]
    
    # Add blank row
    Landcover_fraction.loc[i] = np.nan

    for lc in range(4):
        Landcover_fraction.loc[i][(4*lc)]   = Landcover_area.loc[i][(4*lc)]/LC_area.loc[i][lc]
        Landcover_fraction.loc[i][(4*lc)+1] = Landcover_area.loc[i][(4*lc)+1]/LC_area.loc[i][lc]
        Landcover_fraction.loc[i][(4*lc)+2] = Landcover_area.loc[i][(4*lc)+2]/LC_area.loc[i][lc]
        Landcover_fraction.loc[i][(4*lc)+3] = Landcover_area.loc[i][(4*lc)+3]/LC_area.loc[i][lc]

# Rename index
Landcover_fraction = Landcover_fraction.rename_axis('ARTES_ID')

#%% Recalculate weighted landclass
LC_area['Weighted_LC'] = np.zeros(len(LC_area.index)) # add new column weighted LC 

# Calculate area-weighted landclass 
for i in range(len(LC_area.index)):
    LC_area.iloc[i,5] = 21 * (LC_area.iloc[i,0]/LC_area.iloc[i,4]) + \
                            22 * (LC_area.iloc[i,1]/LC_area.iloc[i,4]) + \
                            23 * (LC_area.iloc[i,2]/LC_area.iloc[i,4]) + \
                            24 * (LC_area.iloc[i,3]/LC_area.iloc[i,4]) 
                            
#%%
# Calculate total landcover areas in each region 

grass_area = landcover_area.iloc[:,1] + \
             landcover_area.iloc[:,5] +  \
             landcover_area.iloc[:,9] + \
             landcover_area.iloc[:,13]  
             
tree_area = landcover_area.iloc[:,0] + \
             landcover_area.iloc[:,4] +  \
             landcover_area.iloc[:,8] + \
             landcover_area.iloc[:,12]  

green_area = landcover_area.iloc[:,0] + landcover_area.iloc[:,1] + \
             landcover_area.iloc[:,4] + landcover_area.iloc[:,5] + \
             landcover_area.iloc[:,8] + landcover_area.iloc[:,9] + \
             landcover_area.iloc[:,12] + landcover_area.iloc[:,13]   
             
green_plus_shrub_area = np.sum(landcover_area.iloc[:,0:3], axis = 1) + \
             np.sum(landcover_area.iloc[:,4:7], axis = 1) + \
             np.sum(landcover_area.iloc[:,8:11], axis = 1) + \
             np.sum(landcover_area.iloc[:,12:15], axis = 1)  

pervious_area = np.sum(landcover_area.iloc[:,0:4], axis = 1) + \
             np.sum(landcover_area.iloc[:,4:8], axis = 1) + \
             np.sum(landcover_area.iloc[:,8:12], axis = 1) + \
             np.sum(landcover_area.iloc[:,12:], axis = 1)
             
#%% Save outputs 

os.chdir(Path to Step 2 Folder)

LC_area.to_csv('landclass_area_providers.csv')
Landcover_area.to_csv('landcover_area_providers.csv')
Landcover_fraction.to_csv('landcover_fraction_providers.csv')
