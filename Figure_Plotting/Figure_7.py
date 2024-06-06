# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import os 
import matplotlib.pyplot as plt

# Import SSP + zoning scenario annual demand projections (Step 4 Folder)

os.chdir(Step 4 Folder)

SSP = "SSP3" # 'SSP3' or 'SSP5'  
scenario = "med" # change to "low" , "med", or "hi"

indoor_demand_proj = pd.read_csv("Provider_projection_indoor_" + SSP + "_" + scenario + ".csv", index_col = 0)
outdoor_demand_proj = pd.read_csv("Provider_projection_outdoor_" + SSP + "_" + scenario + ".csv", index_col = 0)
pop_ssp = pd.read_csv("service_region_population_" + SSP + "_2010_2100.csv", index_col = 0)
historical_use = pd.read_csv("Historical_use_master.csv", index_col = 0)
provider_outdoor_water_props = pd.read_csv("Provider_outdoor_properties.csv", index_col = 0)

#%% Figure 7: Percent increase in population vs demand: 2010 - 2100

columns = ['ID', 'Pop_2010', 'Pop_2100', 'Outdoor_2010', 'Outdoor_2100', 'Indoor_2010', 'Indoor_2100', 
           'Initial_Weighted_LC','Outdoor_frac','grass_frac', 'tree_frac','shrub_frac', 'Final_Weighted_LC']
master_demand_sensitivity = pd.DataFrame(columns = columns)
climate = False
climate_effect = 0.16

for n in range(len(outdoor_demand_proj.iloc[:,0])):
    provider = outdoor_demand_proj.iloc[n,0]
    if provider == 'IRR_SMT':
        continue
    else:     
        pop = pop_ssp.where(pop_ssp.Service_region == provider).dropna()
        if climate == True:
            provider_projection_outdoor = outdoor_demand_proj.where(outdoor_demand_proj.ID == provider).dropna()
            provider_projection_outdoor.iloc[0,1:12] = np.multiply(climate_effect, provider_projection_outdoor.iloc[0,1:12])
            
        else:
           provider_projection_outdoor = outdoor_demand_proj.where(outdoor_demand_proj.ID == provider).dropna()
           
        provider_projection_indoor = indoor_demand_proj.where(indoor_demand_proj.ID == provider).dropna()
        columns = ['Pop_2010', 'Pop_2100', 'Outdoor_2010', 'Outdoor_2100', 'Indoor_2010', 'Indoor_2100', 'Initial_Weighted_LC',
                   'Outdoor_frac','grass_frac', 'tree_frac','shrub_frac', 'Final_Weighted_LC']
        demand_sensitivity = pd.DataFrame(data = np.zeros((1,len(columns))), columns = columns)
        outdoor_frac = provider_outdoor_water_props.where(provider_outdoor_water_props.ID == provider).dropna()
        grass_frac = outdoor_frac.iloc[0,2]
        tree_frac = outdoor_frac.iloc[0,3]
        shrub_frac = outdoor_frac.iloc[0,4]
        demand_sensitivity.iloc[0,:] = np.array(([pop.iloc[0,1], pop.iloc[0,10], provider_projection_outdoor.iloc[0,1], 
                                                  provider_projection_outdoor.iloc[0,10], provider_projection_indoor.iloc[0,1], 
                                                  provider_projection_indoor.iloc[0,10], provider_projection_indoor.iloc[0,11], outdoor_frac.iloc[0,1],
                                                  grass_frac, tree_frac, shrub_frac, provider_projection_indoor.iloc[0,12]]))
        
        demand_sensitivity.insert(0, 'ID', provider)
        master_demand_sensitivity = pd.concat([master_demand_sensitivity, demand_sensitivity])
        
fig, ax = plt.subplots(figsize = (6,4))
cm = plt.cm.get_cmap('RdYlBu_r')
pop_change = np.divide((master_demand_sensitivity.Pop_2100[:] - master_demand_sensitivity.Pop_2010[:]), master_demand_sensitivity.Pop_2010[:])
outdoor_demand_change = np.divide((master_demand_sensitivity.Outdoor_2100[:] - master_demand_sensitivity.Outdoor_2010[:]), master_demand_sensitivity.Outdoor_2010[:])
total_demand_change = np.divide(((master_demand_sensitivity.Outdoor_2100[:] + master_demand_sensitivity.Indoor_2100[:]) - (master_demand_sensitivity.Outdoor_2010[:] + master_demand_sensitivity.Indoor_2010[:])), (master_demand_sensitivity.Outdoor_2010[:] + master_demand_sensitivity.Indoor_2010[:]))



fig, ax = plt.subplots(figsize = (6,4))
cm = plt.cm.get_cmap('RdYlBu_r')
plt.plot([-200,200],[-200,200], color = 'k')
plt.plot([-200,200],[-100,100], color = 'k')
plt.plot([-200,200],[-66,66], color = 'k')
plt.plot([-200,200],[-50,50], color = 'k')
sc = ax.scatter(100*pop_change.values , 100*total_demand_change.values, c = np.divide(master_demand_sensitivity.Outdoor_2010[:],(master_demand_sensitivity.Outdoor_2010[:] + master_demand_sensitivity.Indoor_2010[:])), cmap = cm)
plt.grid()
plt.colorbar(sc, label = 'Initial % outdoor use')
# plt.ylim([-20, 100]) # For SSP5
# plt.xlim([0, 150]) # For SSP5
plt.ylim([-100,10]) # For SSP3
plt.xlim([-100, 0]) # For SSP3
plt.ylabel('% change in demand')
plt.xlabel('% change in population')






