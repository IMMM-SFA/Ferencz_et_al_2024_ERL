# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import os 

#%% Import urban growth and population datasets 

SSP = "SSP5" # SSP3 or SSP5 
scenario = 'med'

# Import urban growth projection for specific SSP scenario - Step 1c
os.chdir(Path to Step 1c Folder + SSP) # insert path to Step 1c folder, plus SSP name to navigate to the correct subfolder 

LU_df = pd.read_csv(SSP + "_Aggregated_landclass_projection_data.csv", index_col = 0)

for i in range(len(LU_df.iloc[:,0])):
    if LU_df.Provider_ID[i][0:7] == 'IOU_PWC':
        LU_df.Provider_ID[i] = 'IOU_PWC'
    elif LU_df.Provider_ID[i][0:11] == 'IOU_SWS_WLM':
        LU_df.Provider_ID[i] = 'IOU_SWS_WLM'
    else:
        continue 

# Import 2019 NLCD data - Step 1a 
os.chdir(Path to Step_1a Folder)
NLCD_historic = pd.read_csv("NLCD_LC_areas_historic.csv")

#%% Land class areas for all LA or optionally a single water provider. 

provider = 'CTY_CPT' # OPTIONAL - comment out 'filter by provider' if want results for ALL of LA, for Figure 5 use CTY_CPT or CWD_WVA
title = provider # Make "LA" or all providers and comment out Lines 33, 41, and 42

filtered = LU_df.copy()
filtered = filtered.dropna()
filtered = filtered.where(filtered.scenario == scenario)
filtered = filtered.dropna()

# filter by provider (OPTIONAL), comment out Lines 41 and 42 if wanting to plot for results for all of LA 
filtered = filtered.where(filtered.Provider_ID == provider)
filtered = filtered.dropna()

filtered_21 = filtered.copy()
filtered_21 = filtered_21.where(filtered_21.urban_class == 21)
filtered_21 = filtered_21.dropna()
filtered_22 = filtered.copy()
filtered_22 = filtered_22.where(filtered_22.urban_class == 22)
filtered_22 = filtered_22.dropna()
filtered_23 = filtered.copy()
filtered_23 = filtered_23.where(filtered_23.urban_class == 23)
filtered_23 = filtered_23.dropna()
filtered_24 = filtered.copy()
filtered_24 = filtered_24.where(filtered_24.urban_class == 24)
filtered_24 = filtered_24.dropna()

# filter NLCD historic by provider (OPTIONAL)
filtered_NLCD = NLCD_historic.copy()
filtered_NLCD = filtered_NLCD.where(filtered_NLCD.Service_region == provider)
filtered_NLCD = filtered_NLCD.dropna()

# Urban projections - Area (km^2) - Used for future total LC area km^2 in Figure 4 (all LA)
Fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(1,8))
i = 6 # column index (decade), 6 = 2020
axs.fill_between([1,2], np.sum(900/10**6 * np.concatenate((filtered_24.iloc[:,i], filtered_23.iloc[:,i], filtered_22.iloc[:, i], filtered_21.iloc[:,i]), axis = 0), axis = 0), color = 'black', label = '24')
axs.fill_between([1,2], np.sum(900/10**6 * np.concatenate((filtered_23.iloc[:,i], filtered_22.iloc[:,i], filtered_21.iloc[:,i]), axis = 0), axis = 0), color = 'gray', label = '23')
axs.fill_between([1,2], np.sum(900/10**6 * np.concatenate((filtered_22.iloc[:,i], filtered_21.iloc[:,i]), axis = 0), axis = 0), color = 'silver', label = '22')
axs.fill_between([1,2], np.sum(900/10**6 * np.array(filtered_21.iloc[:,i].values).astype('int'), axis = 0), color = 'gainsboro', label = '21')
axs.set_ylabel('Area km^2')
#axs.set_ylim([0, 3000])
axs.set_title(title)
plt.grid(visible = True)

# Historic 2019 NLCD - Area (km^2) - Used for initial total LC area km^2 in Figure 4 (all LA)
Fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(1,8))
axs.fill_between([1,2], np.sum(900/10**6 * np.concatenate((filtered_NLCD.iloc[:,4], filtered_NLCD.iloc[:,3], filtered_NLCD.iloc[:,2], filtered_NLCD.iloc[:,1]), axis = 0), axis = 0), color = 'maroon', label = '24')
axs.fill_between([1,2], np.sum(900/10**6 * np.concatenate((filtered_NLCD.iloc[:,3], filtered_NLCD.iloc[:,2], filtered_NLCD.iloc[:,1]), axis = 0), axis = 0), color = 'goldenrod', label = '23')
axs.fill_between([1,2], np.sum(900/10**6 * np.concatenate((filtered_NLCD.iloc[:,2], filtered_NLCD.iloc[:,1]), axis = 0), axis = 0), color = 'mediumseagreen', label = '22')
axs.fill_between([1,2], np.sum(900/10**6 * np.array(filtered_NLCD.iloc[:,1].values).astype('int'), axis = 0), color = 'cornflowerblue', label = '21')
axs.set_ylabel('Area km^2')
#axs.set_ylim([0,70])
axs.set_title(title)
plt.grid(visible = True)

# Historic 2019 NLCD - Area (%) - Used for initial LC area fractions in Figure 5
Fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(1,8))
total_provider_urban_area = np.sum(900/10**6 * np.concatenate((filtered_NLCD.iloc[:,4], filtered_NLCD.iloc[:,3], filtered_NLCD.iloc[:,2], filtered_NLCD.iloc[:,1]), axis = 0), axis = 0)
axs.fill_between([1,2], np.sum(900/10**6 * np.concatenate((filtered_NLCD.iloc[:,4], filtered_NLCD.iloc[:,3], filtered_NLCD.iloc[:,2], filtered_NLCD.iloc[:,1]), axis = 0), axis = 0)/total_provider_urban_area, color = 'black', label = '24')
axs.fill_between([1,2], np.sum(900/10**6 * np.concatenate((filtered_NLCD.iloc[:,3], filtered_NLCD.iloc[:,2], filtered_NLCD.iloc[:,1]), axis = 0), axis = 0)/total_provider_urban_area, color = 'gray', label = '23')
axs.fill_between([1,2], np.sum(900/10**6 * np.concatenate((filtered_NLCD.iloc[:,2], filtered_NLCD.iloc[:,1]), axis = 0), axis = 0)/total_provider_urban_area, color = 'silver', label = '22')
axs.fill_between([1,2], np.sum(900/10**6 * np.array(filtered_NLCD.iloc[:,1].values).astype('int'), axis = 0)/total_provider_urban_area, color = 'gainsboro', label = '21')
axs.set_ylabel('Urban area % LC')
axs.set_ylim([0,1])
axs.set_title(title)
plt.grid(visible = True)

# Urban projections - Area (%). Used for 2100 LC area fractions in Figures 5 
Fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(1,8))
i = 14 # column index (decade), 14 = 2100
total_provider_urban_area = np.sum(900/10**6 * np.concatenate((filtered_24.iloc[:,i], filtered_23.iloc[:,i], filtered_22.iloc[:, i], filtered_21.iloc[:,i]), axis = 0), axis = 0)
axs.fill_between([1,2], np.sum(900/10**6 * np.concatenate((filtered_24.iloc[:,i], filtered_23.iloc[:,i], filtered_22.iloc[:, i], filtered_21.iloc[:,i]), axis = 0), axis = 0)/total_provider_urban_area, color = 'black', label = '24')
axs.fill_between([1,2], np.sum(900/10**6 * np.concatenate((filtered_23.iloc[:,i], filtered_22.iloc[:,i], filtered_21.iloc[:,i]), axis = 0), axis = 0)/total_provider_urban_area, color = 'gray', label = '23')
axs.fill_between([1,2], np.sum(900/10**6 * np.concatenate((filtered_22.iloc[:,i], filtered_21.iloc[:,i]), axis = 0), axis = 0)/total_provider_urban_area, color = 'silver', label = '22')
axs.fill_between([1,2], np.sum(900/10**6 * np.array(filtered_21.iloc[:,i].values).astype('int'), axis = 0)/total_provider_urban_area, color = 'gainsboro', label = '21')
axs.set_ylabel('Urban area % LC')
axs.set_ylim([0, 1])
axs.set_title(title)
plt.grid(visible = True)




