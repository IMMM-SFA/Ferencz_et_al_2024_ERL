# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import os 
import geopandas
import contextily as cx
import rasterio
from rasterio.mask import mask
from rasterio.plot import show

os.chdir(Path to Step_3 folder)

# Import service regions boundaries 
service_bnds = geopandas.read_file("Artes_service_regions_updated.shp")  
service_bnds = service_bnds.to_crs(epsg=3857) # convert CRS to basemap CRS 
service_bnds = service_bnds.where(service_bnds.Artes_se_3 == 1)
service_bnds = service_bnds.dropna(thresh = 3)
service_bnds = service_bnds.reset_index(drop = True)
service_ids = service_bnds.Artes_serv

#%% Difference rasters to determine urban cells whose urban land class changed (urban conversion = intensification)

SSP = "SSP5" # SSP3 or SSP5
scenario = "med" # low, med, or hi

# Import urban landclass rasters
        
# Visualize clipped region 
raster_2100 = rasterio.open(SSP + "_" + scenario + "_2100.tif")
raster_2010 = rasterio.open(SSP + "_" + scenario + "_2010.tif")
# show(raster_2100)
# show(raster_2010)

# Filter for urban landclass values (band values 21 to 24)
raster_2100_array = raster_2100.read()
raster_2100_array = np.where(raster_2100_array < 25, raster_2100_array, np.nan)
raster_2100_array = np.where(raster_2100_array > 20, raster_2100_array, np.nan)
#plt.imshow(raster_2100_array[0,:,:]) # plot filtered raster 

raster_2010_array = raster_2010.read()
raster_2010_array = np.where(raster_2010_array < 25, raster_2010_array, np.nan)
raster_2010_array = np.where(raster_2010_array > 20, raster_2010_array, np.nan)
#plt.imshow(raster_2010_array[0,:,:]) # plot filtered raster 

# Difference rasters to determine urban cells whose land class changed 
raster_difference = raster_2100_array - raster_2010_array
#raster_difference[np.isnan(raster_difference) == True] = 100 # use 100 as no data value for producing rasters for QGIS 
raster_difference = np.where(raster_difference != 0, raster_difference, np.nan) # 
# raster_difference = np.where(raster_difference < 0, raster_difference, np.nan) # only use for SSP3 to query for de-intensification, pixels whose urban LC declined will have a negative value, comment out line above if this is chosen

#raster_difference[raster_difference == 0] = np.nan
current_cmap = mpl.cm.get_cmap('viridis')
current_cmap.set_bad(color='white')
plt.imshow(raster_difference[0,:,:], interpolation='none', cmap = current_cmap, vmin = 0, vmax = 3)
plt.colorbar()

src = rasterio.open(SSP + "_" + scenario + "_2100.tif") # Clone raster georeference and source information
raster_difference = np.where(raster_difference > -2, raster_difference, 100) 

# Register GDAL format drivers and configuration options with a
# context manager.
with rasterio.Env():

    # Write an array as a raster band to a new 8-bit file. For
    # the new file's profile, we start with the profile of the source
    profile = src.profile
    profile['nodata'] = 100
    # And then change the band count to 1, set the
    # dtype to uint8, and specify LZW compression.
    profile.update(
        dtype=rasterio.uint16,
        count=1,
        compress='lzw')

    with rasterio.open('Urban_intensification_' + SSP +'_' + scenario + '.tif', 'w', **profile) as dst:
        dst.write(raster_difference[0,:,:].astype(rasterio.uint16), 1)


#%% New Urban land (urban growth)

# Filter for urban landclass values (band values 21 to 24)
# Urban cells at ending year indicated by binary 1 or nan
raster_2100_array = raster_2100.read()
raster_2100_array[raster_2100_array == -32768] = 50
raster_2100_array = np.where(raster_2100_array < 25, 21, np.nan) # urban land = 21, other land = nan
raster_2100_array = np.where(raster_2100_array > 20, 21, np.nan) # urban land = 21, other land = nan
raster_2100_array[raster_2100_array == 21] = 1
#plt.imshow(raster_2100_array[0,:,:], interpolation='none') # plot filtered raster 

# Filter for urban landclass values (band values 21 to 24)
# Non-urban cells assigned value of 2 
raster_2010_array = raster_2010.read()

raster_2010_array = np.where(raster_2010_array == -32768, np.nan, raster_2010_array)
raster_2010_array = np.where(raster_2010_array > 25, 2, raster_2010_array)
raster_2010_array = np.where(raster_2010_array < 20, 2, raster_2010_array)
raster_2010_array[raster_2010_array == 21] = 1
raster_2010_array[raster_2010_array == 22] = 1
raster_2010_array[raster_2010_array == 23] = 1
raster_2010_array[raster_2010_array == 24] = 1
#plt.imshow(raster_2010_array[0,:,:], interpolation='none') # plot filtered raster 


# Difference rasters to determine urban cells whose land class changed 
raster_difference = raster_2010_array - raster_2100_array
#raster_difference[np.isnan(raster_difference) == True] = 100 # use 100 as no data value for producing rasters for QGIS 
raster_difference = np.where(raster_difference == 0, np.nan, raster_difference) # use if plotting in Python 
#raster_difference[raster_difference == 0] = np.nan
current_cmap = mpl.cm.get_cmap('Greys')
current_cmap.set_bad(color='white')
plt.imshow(raster_difference[0,:,:], interpolation='none', cmap = current_cmap, vmin = 0, vmax = 1)
plt.colorbar()

# Save array ("raster_difference") as a raster 

src = rasterio.open(SSP + "_" + scenario + "_2100.tif") # Clone raster georeference and source information
raster_difference = np.where(raster_difference > -2, raster_difference, 100) 


# Register GDAL format drivers and configuration options with a
# context manager.
with rasterio.Env():

    # Write an array as a raster band to a new 8-bit file. For
    # the new file's profile, we start with the profile of the source
    profile = src.profile
    profile['nodata'] = 100
    # And then change the band count to 1, set the
    # dtype to uint8, and specify LZW compression.
    profile.update(
        dtype=rasterio.uint16,
        count=1,
        compress='lzw')

    with rasterio.open('Urban_growth_' + SSP +'_' + scenario + '.tif', 'w', **profile) as dst:
        dst.write(raster_difference[0,:,:].astype(rasterio.uint16), 1)
    

