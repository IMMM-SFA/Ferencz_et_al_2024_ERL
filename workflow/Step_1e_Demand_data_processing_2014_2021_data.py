# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 14:23:31 2023

@author: fere556
"""

import os 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

os.chdir('C:/Users/fere556/OneDrive - PNNL/Documents/Artes/Demand_Paper/Provider_Historical_Demands')

monthly_data = pd.read_csv('Artes_node_monthly_delivery_data_CA_database.csv', 
                           thousands = ',')

artes_annual_data = pd.read_csv('Artes_node_IDs_monthly_delivery_data_CA_database.csv')

artes_demands = pd.read_csv('Artes_original_demands.csv')

demand_update_table = pd.read_csv('Demand_update_table.csv')

# Provider Names
Providers = monthly_data.iloc[:,1].unique()

# Monthly supply in AF
monthly_data['Supply_acft'] = np.zeros((monthly_data.iloc[:,0].size))

# Convert all monthly supply volumes to ACFT 
volume_units = monthly_data.iloc[:,13].unique()


for row in range(monthly_data.iloc[:,0].size):
    print(row)
    if monthly_data.iloc[row,13] == 'AF':
        monthly_data.Supply_acft[row] = monthly_data.iloc[row,15]
     
    # convert CCF (100 ft^3) to Acre feet
    elif monthly_data.iloc[row,13] == 'CCF':
        monthly_data.Supply_acft[row] = (2.83 * monthly_data.iloc[row,15])/1233.48 
    
    # convert MG to Acre feet
    elif monthly_data.iloc[row,13] == 'MG':
        monthly_data.Supply_acft[row] = monthly_data.iloc[row,15]/.325851
    
    # convert G to Acre feet 
    elif monthly_data.iloc[row,13]  == 'G':
        monthly_data.Supply_acft[row] = monthly_data.iloc[row,15]/325851      
   

# Create DataFrame for monthly supply data for each provider 

# Iterate through each provider name
# Only use data from 2017 to 2021
# Aggregate data by month into a list (months in spreadsheet are numeric)

practice_df = pd.DataFrame(data = None, columns = ['Provider','Jan','Feb', 'Mar', 'Apr',
                      'May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])


for provider in Providers:
    filter_df = monthly_data.copy()
    filter_df = filter_df.where(filter_df.Artes_NODE_ID_1[:] == provider)
    filter_df = filter_df.dropna(thresh = 15)
    filter_df = filter_df.where(filter_df.Year_5[:].astype('int') > 2013)
    filter_df = filter_df.dropna(thresh = 15)
    filter_df = filter_df.where(filter_df.Year_5[:].astype('int') < 2022)
    filter_df = filter_df.dropna(thresh = 15)
    
    # List of lists to store monthly supply values, resets each loop
    month_list = [[],[],[],[],[],[],[],[],[],[],[],[]]
    
    for month in range(12):
        month_df = filter_df.copy()
        month_df = month_df.where(month_df.Month_4[:].astype('int') == month+1)
        month_df = month_df.dropna(thresh = 16)
        
        temp = []
        for j in range(month_df.Supply_acft[:].size):
            if np.isnan(month_df.iloc[j,30]) == 0:
                temp.append(month_df.iloc[j,30])
            else:
                continue
            
        month_list[month] = temp
        

    practice_df = practice_df.append({'Provider': provider, 'Jan' : month_list[0], 
                    'Feb' : month_list[1], 'Mar' : month_list[2], 'Apr' : month_list[3], 
                    'May' : month_list[4], 'Jun' : month_list[5], 'Jul' : month_list[6],
                    'Aug' : month_list[7], 'Sep' : month_list[8], 'Oct' : month_list[9], 
                    'Nov' : month_list[10], 'Dec' : month_list[11]},
            ignore_index = True)


# Calculate avg, min, and max monthly supply for each provider
monthly_use_avg = np.zeros((len(Providers),12))
monthly_use_min = np.zeros((len(Providers),12))
monthly_use_max = np.zeros((len(Providers),12))

for row in range(practice_df.iloc[:,0].size):
    for month in range(12):
        monthly_use_avg[row,month] = np.mean(practice_df.iloc[row, month+1])
        monthly_use_min[row,month] = np.min(practice_df.iloc[row, month+1])
        monthly_use_max[row,month] = np.max(practice_df.iloc[row, month+1])

# Calculate avg, min, and max annual supply for each provider 
annual_avg_arr = np.zeros((len(Providers),1))
annual_min_arr = np.zeros((len(Providers),1))
annual_max_arr = np.zeros((len(Providers),1))

for row in range(practice_df.iloc[:,0].size):
    annual_avg_arr[row] = np.sum(monthly_use_avg[row,:])
    annual_min_arr[row] = np.sum(monthly_use_min[row,:])
    annual_max_arr[row] = np.sum(monthly_use_max[row,:])

# Merge calculated monthly demands with provider name
# avg
monthly_demands_updated_avg = pd.DataFrame(data = monthly_use_avg.copy(), columns = ['Jan','Feb', 'Mar', 'Apr',
                      'May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
monthly_demands_updated_avg['Provider'] = Providers

# min
monthly_demands_updated_min = pd.DataFrame(data = monthly_use_min.copy(), columns = ['Jan','Feb', 'Mar', 'Apr',
                      'May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
monthly_demands_updated_min['Provider'] = Providers

# max
monthly_demands_updated_max = pd.DataFrame(data = monthly_use_max.copy(), columns = ['Jan','Feb', 'Mar', 'Apr',
                      'May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
monthly_demands_updated_max['Provider'] = Providers

#%% Time series from 2014 to 2022 for each provider 

annual_arr = np.zeros((len(Providers),7)) 

for i in range(len(Providers)):
    filter_df = monthly_data.copy()
    filter_df = filter_df.where(filter_df.Artes_NODE_ID_1[:] == Providers[i])
    filter_df = filter_df.dropna(thresh = 15)
    for year in range(7):
        monthly_values = filter_df.where(filter_df.Year_5 == year+2015)
        monthly_values = monthly_values.dropna(thresh = 15)
        if np.nan in monthly_values.iloc[:,30].values:
            continue
        else:
            annual_arr[i,year] = np.sum(monthly_values.iloc[:,30])

count = 0
fig, axs = plt.subplots(nrows=8, ncols=7, figsize=(12, 12))
rows = np.sort(np.tile(np.arange(8),7))
cols = np.tile(np.arange(7),8)
for i in range(len(Providers)):
    if min(annual_arr[i,:])/max(annual_arr[i,:]) < .7:
        continue 
    else:
        axs[rows[count], cols[count]].plot(np.arange(7)+2015, annual_arr[i,:]/max(annual_arr[i,:]), alpha = 0.5)
        axs[rows[count], cols[count]].scatter(np.arange(7)+2015, annual_arr[i,:]/max(annual_arr[i,:]))
        axs[rows[count], cols[count]].set_title(Providers[i])
        axs[rows[count], cols[count]].set_ylim([0.7, 1])
        axs[rows[count], cols[count]].yaxis.set_major_locator(MultipleLocator(.1))
        axs[rows[count], cols[count]].yaxis.set_minor_locator(MultipleLocator(.05))
        axs[rows[count], cols[count]].xaxis.set_major_locator(MultipleLocator(5))
        axs[rows[count], cols[count]].xaxis.set_minor_locator(MultipleLocator(1))
        count += 1
       
        
plt.tight_layout()

# count = 0
# fig, axs = plt.subplots(nrows=8, ncols=7, figsize=(12, 12))
# rows = np.sort(np.tile(np.arange(8),7))
# cols = np.tile(np.arange(7),8)
# for i in range(len(Providers)):
#     if min(annual_arr[i,:])/max(annual_arr[i,:]) < .7:
#         continue 
#     else:
#         axs[rows[count], cols[count]].plot(np.arange(7)+2015, annual_arr[i,:], alpha = 0.5, c = 'r')
#         axs[rows[count], cols[count]].scatter(np.arange(7)+2015, annual_arr[i,:], alpha = 0.5, c = 'r')
#         count += 1

# plt.tight_layout()
        
#%% Generate new Demands table for Artes 

# Create new demand table with updated node list
node_IDs = demand_update_table.ID.unique()
node_IDs_count = np.zeros(len(node_IDs))
for i in range(len(node_IDs)):
    count = 0
    for j in range(len(demand_update_table.ID)):
        if node_IDs[i] == demand_update_table.ID[j]:
            count += 1
    node_IDs_count[i] = count
    
data = np.zeros((len(node_IDs),13))
demands = pd.DataFrame(data = data.copy(), columns = ['Annual','Jan','Feb', 'Mar', 'Apr',
                      'May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
demands.insert(loc = 0, column = 'ID', value = node_IDs)

# Use updated data when available, otherwise use Artes monthly data

# Iterate through list of root node IDs from 'demand_root' column in 
# demand_updates df matches a Provider name in monthly_demands_updated_XXX 
# (XXX = avg, min, or max) Dataframe. If there is a match, use updated data. 
# If there is not a match, find monthly demands in artes_demands df. 
# Assign indoor and outdoor demands based on min monthly use. NOTE: For the 
# demand projection analysis, the indoor and outdoor components are summmed 
# and only the total monthly values are use. The partitioning between indoor 
# and outdoor demand happens within the demand projection script 
# "Future_demand_landcover_evolution.py"

root_IDs = demand_update_table.Demand_Root.unique()
updated_demand_data = monthly_demands_updated_min # choose min, max, or avg

for root_ID in root_IDs:
    
    # Does node have indoor and outdoor demand?
    demand_types = demand_update_table.where(demand_update_table.Demand_Root == root_ID)
    demand_types = demand_types.dropna(thresh = 2)
    indexes = demand_types.index
    
    # Check if root node has updated demand data 
    if root_ID in updated_demand_data.Provider.unique():
        
        if len(demand_types.iloc[:,0]) == 2:
            data = updated_demand_data.where(updated_demand_data.Provider == root_ID)
            data = data.dropna()
            indoor = min(data.iloc[0,0:12].values) # find min monthly use
            outdoor = data.iloc[0,0:12].values - indoor # monthly outdoor use is total use minus indoor use
            indoor = indoor * np.ones((1,12)) # array of calculated monthly indoor use 
            
            # Assign indoor and outdoor use to demands dataframe
            demands.iloc[indexes[0],2:] = indoor[0,:]
            demands.iloc[indexes[0],1] = np.sum(indoor)
            demands.iloc[indexes[1],2:] = outdoor[:]
            demands.iloc[indexes[1],1] = np.sum(outdoor)
            
        else: # Assign all demand to only one node (either single outdoor, single indoor, or single non categorized )
            data = updated_demand_data.where(updated_demand_data.Provider == root_ID)
            data = data.dropna()    
            total = data.iloc[0,0:12].values
            demands.iloc[indexes[0], 2:] = total[0,:]
            demands.iloc[indexes[0],1] = np.sum(total)
    
    # If no updated monthly use data, use Artes data 
    elif root_ID in artes_demands.Node.unique():
        
        if len(demand_types.iloc[:,0]) == 2:
            data = artes_demands.where(artes_demands.Node == root_ID)
            data = data.dropna()
            indoor = min(data.iloc[0,2:].values) # find min monthly use
            outdoor = data.iloc[0,2:].values - indoor # monthly outdoor use is total use minus indoor use
            indoor = indoor * np.ones((1,12)) # array of calculated monthly indoor use 
            
            # Assign indoor and outdoor use to demands dataframe
            demands.iloc[indexes[0],2:] = indoor[0,:]
            demands.iloc[indexes[0],1] = np.sum(indoor)
            demands.iloc[indexes[1],2:] = outdoor[:]
            demands.iloc[indexes[1],1] = np.sum(outdoor)
            
        else: # Assign all demand to only one node (either single outdoor, single indoor, or single non categorized )
            data = artes_demands.where(artes_demands.Node == root_ID)
            data = data.dropna()    
            total = data.iloc[0,2:].values
            demands.iloc[indexes[0], 2:] = total[:]
            demands.iloc[indexes[0],1] = np.sum(total)
    
    else:
        
        continue 
    
demands.to_csv('Provider_historical_demands_min.csv') # modify file name for demand scenario (min, max, avg)
    
    
#%% Create DataFrame to compare recent annual average supply (2017-2021) to 
# annual average supply used in Artes (2010) 
annual_comparison = pd.DataFrame(data = None, columns = ['Provider', 'recent_avg',
                            'artes_avg'])

annual_comparison.Provider = Providers
annual_comparison.recent_avg = annual_avg_arr

for i in range(len(Providers)):
    provider = annual_comparison.Provider[i] 
    artes_copy = artes_annual_data.copy()
    artes_copy = artes_copy.where(artes_copy.Ca_database_name[:] == provider)
    artes_copy = artes_copy.dropna(thresh = 6)
    annual_comparison.iloc[i,2] = artes_copy.iloc[0,5]

np.sum(annual_comparison.artes_avg[:])
np.sum(annual_comparison.recent_avg[:])
    
#%% Plotting 

# Monthly use min, max, avg for a provider 
fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(6, 4))
row = 16 
axs.plot(np.arange(12)+1, monthly_use_arr[row,:]) 
axs.plot(np.arange(12)+1, monthly_use_min[row,:]) 
axs.plot(np.arange(12)+1, monthly_use_max[row,:])

# % diff between max and min and the average annual use 
fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(6, 4)) 
axs.scatter(np.arange(75), (annual_max_arr[:] - annual_avg_arr[:])/annual_avg_arr[:]) 
axs.scatter(np.arange(75), (annual_min_arr[:] - annual_avg_arr[:])/annual_avg_arr[:]) 

# Boxplot of % increase and decrease for min and max compared to avg 
fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(2, 4))
plt.boxplot(100*(annual_min_arr[:] - annual_avg_arr[:])/annual_avg_arr[:])
plt.boxplot(100*(annual_max_arr[:] - annual_avg_arr[:])/annual_avg_arr[:])
plt.ylabel("% diff from average annual use")



# Monthly use factors 
fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(6, 4))
for row in range(practice_df.iloc[:,0].size):
    axs.plot(np.arange(12)+1, monthly_use_arr[row,:]/annual_avg_arr[row]) #, label = 'Imports', color = 'blue')

# Monthly use factors 
row = 16
fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(6, 4))
axs.plot(np.arange(12)+1,  monthly_use_arr[row,:]/annual_avg_arr[row]) 

# Relative monthly useage
fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(6, 4))
for row in range(practice_df.iloc[:,0].size):
    axs.plot(np.arange(12)+1, monthly_use_arr[row,:]/min(monthly_use_arr[row,:])) 
    
# Relative monthly useage
row = 16
fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(6, 4))
axs.plot(np.arange(12)+1, monthly_use_arr[row,:]/min(monthly_use_arr[row,:])) 

# Indoor use 
total_indoor = 0 
fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(6, 4))
for row in range(practice_df.iloc[:,0].size):
    axs.scatter(1,min(monthly_use_arr[row,:])) #, label = 'Imports', color = 'blue')
    total_indoor += np.sum(12*min(monthly_use_arr[row,:]))
    
# Outdoor use 
total_outdoor = 0
fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(6, 4))
for row in range(practice_df.iloc[:,0].size):
    axs.scatter(np.arange(12)+1,monthly_use_arr[row,:]-min(monthly_use_arr[row,:])) #, label = 'Imports', color = 'blue')
    total_outdoor += np.sum(monthly_use_arr[row,:]-min(monthly_use_arr[row,:]))


# Compare Artes annual demand to more recent annual demand (2017-2021)
fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(6, 4))
axs.scatter(np.arange(len(annual_comparison.Provider))+1, -100*(annual_comparison.artes_avg - annual_comparison.recent_avg)/ \
           annual_comparison.artes_avg) 
axs.yaxis.set_major_locator(MultipleLocator(20))
axs.yaxis.set_minor_locator(MultipleLocator(10))
#axs.plot()
plt.grid(which = 'both', axis = 'y')
    



