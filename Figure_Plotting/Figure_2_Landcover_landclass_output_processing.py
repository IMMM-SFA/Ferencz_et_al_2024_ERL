# -*- coding: utf-8 -*-

import os 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

os.chdir(Path to Step 2 Folder) # path to Step 2 folder 

landclass_area = pd.read_csv('landclass_area_providers.csv', index_col = 0)
landcover_area = pd.read_csv('landcover_area_providers.csv', index_col = 0)
landcover_fraction = pd.read_csv('landcover_fraction_providers.csv', index_col = 0)

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

region_count = len(landclass_area.iloc[:,0])
grass_frac = np.zeros(region_count)
tree_frac = np.zeros(region_count)
green_frac = np.zeros(region_count)
green_plus_shrub_frac = np.zeros(region_count)

for i in range(region_count):
    
    grass_frac[i] = grass_area[i]/landclass_area.All_LC[i]
    tree_frac[i] = tree_area[i]/landclass_area.All_LC[i]
    green_frac[i] = green_area[i]/landclass_area.All_LC[i]
    green_plus_shrub_frac[i] =  green_plus_shrub_area[i]/landclass_area.All_LC[i]     


#%% Plots Figure 2

# Figure 2 subplot b: Service region weighted Land Class vs landcover fraction 
plt.figure()
plt.scatter(landclass_area.Weighted_LC, green_plus_shrub_frac, color = 'k')
plt.ylabel('Green fraction urban land')
plt.xlabel('Weighted average urban LC')

# Optial other versions of the subplot b showing 
# plt.figure()
# plt.scatter(landclass_area.Weighted_LC, green_frac) # tree + grass

# plt.figure()
# plt.scatter(landclass_area.Weighted_LC, grass_frac) # grass only 

# plt.figure()
# plt.scatter(landclass_area.Weighted_LC, tree_frac) # tree only 


# Figure 2 subplot c: 
plt.figure()
for i in range(89):
    if landcover_fraction.index[i] != 'CWD_SAV':
        plt.plot(np.arange(4), [np.sum(landcover_fraction.iloc[i, 0:3]), np.sum(landcover_fraction.iloc[i, 4:7]), 
                            np.sum(landcover_fraction.iloc[i, 8:11]), np.sum(landcover_fraction.iloc[i, 12:15])], color = 'k', 
                 alpha = 0.1)
        plt.xticks([0,1,2,3], labels = ['LC 21', 'LC 22', 'LC 23', 'LC 24'])

plt.ylabel('Green fraction urban land')
plt.xlabel('Weighted average urban LC')

