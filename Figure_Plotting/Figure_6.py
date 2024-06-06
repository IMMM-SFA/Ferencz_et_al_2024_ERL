# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import os 
import matplotlib.pyplot as plt
import geopandas

os.chdir(Step 4 Folder)

SSP = "SSP5" # 'SSP3' or 'SSP5'  
scenario = "med" # change to "low" , "med", or "hi"

indoor_demand_proj = pd.read_csv("Provider_projection_indoor_" + SSP + "_" + scenario + ".csv")
outdoor_demand_proj = pd.read_csv("Provider_projection_outdoor_" + SSP + "_" + scenario + ".csv")
pop_ssp = pd.read_csv("service_region_population_" + SSP + "_2010_2100.csv", index_col = 0)
historical_use = pd.read_csv("Historical_use_master.csv", index_col = 0)

service_bnds = geopandas.read_file("Artes_service_regions_updated.shp")  
service_bnds = service_bnds.to_crs(epsg=3857) # convert CRS to basemap CRS 
service_bnds = service_bnds.where(service_bnds.Artes_se_3 == 1)
service_bnds = service_bnds.dropna(thresh = 3)
service_bnds = service_bnds.reset_index(drop = True)

#%% Generate Maps for Figure 6 

# Add columns to track increase in total demand and change in outdoor demand 
service_bnds['growth_tot_demand'] = np.nan * np.zeros(len(service_bnds.iloc[:,0]))
service_bnds['growth_out_demand'] = np.nan * np.zeros(len(service_bnds.iloc[:,0]))
service_bnds['perc_growth_tot_demand'] = np.nan * np.zeros(len(service_bnds.iloc[:,0]))
service_bnds['perc_growth_out_demand'] = np.nan * np.zeros(len(service_bnds.iloc[:,0]))
service_bnds['init_AW_LC'] = np.nan * np.zeros(len(service_bnds.iloc[:,0]))
service_bnds['final_AW_LC'] = np.nan * np.zeros(len(service_bnds.iloc[:,0]))
service_bnds['pop_growth'] = np.nan * np.zeros(len(service_bnds.iloc[:,0]))
service_bnds['init_perc_outdoor'] = np.nan * np.zeros(len(service_bnds.iloc[:,0]))
service_bnds['final_perc_outdoor'] = np.nan * np.zeros(len(service_bnds.iloc[:,0]))
service_bnds['per_capita_initial'] = np.nan * np.zeros(len(service_bnds.iloc[:,0]))
service_bnds['per_capita_final'] = np.nan * np.zeros(len(service_bnds.iloc[:,0]))


for provider in range (len(outdoor_demand_proj.iloc[:,0])):
    if outdoor_demand_proj.ID[provider] == 'IRR_SMT' or outdoor_demand_proj.ID[provider] == 'CTY_SFS' or outdoor_demand_proj.ID[provider] == 'CTY_VER':
        continue
    total_demand_growth = (outdoor_demand_proj.iloc[provider,11] + indoor_demand_proj.iloc[provider,11]) - (outdoor_demand_proj.iloc[provider,2] + indoor_demand_proj.iloc[provider,2])
    outdoor_demand_growth = outdoor_demand_proj.iloc[provider,11] - outdoor_demand_proj.iloc[provider,2]
    percent_total_demand_growth = ((outdoor_demand_proj.iloc[provider,11] + indoor_demand_proj.iloc[provider,11]) - (outdoor_demand_proj.iloc[provider,2] + indoor_demand_proj.iloc[provider,2]))/(outdoor_demand_proj.iloc[provider,2] + indoor_demand_proj.iloc[provider,2])
    percent_outdoor_demand_growth = (outdoor_demand_proj.iloc[provider,11] - outdoor_demand_proj.iloc[provider,2])/outdoor_demand_proj.iloc[provider,2]
    initial_weighted_LC = outdoor_demand_proj.iloc[provider,12]
    final_weighted_LC = outdoor_demand_proj.iloc[provider,13]
    provider_pop = pop_ssp.where(pop_ssp.Service_region[:] == outdoor_demand_proj.ID[provider])
    provider_pop = provider_pop.dropna()
    pop_growth = (provider_pop.iloc[0,10] - provider_pop.iloc[0,1])/provider_pop.iloc[0,1]
    demand_hist = historical_use.copy()
    demand_hist = demand_hist.where(demand_hist.ID == outdoor_demand_proj.ID[provider])
    demand_hist = demand_hist.dropna()
    per_capita_initial = sum(demand_hist.iloc[0,1:])/provider_pop.iloc[0,1]
    per_capita_final = (outdoor_demand_proj.iloc[provider,11] + indoor_demand_proj.iloc[provider,11])/provider_pop.iloc[0,10]
    
    for j in range(len(service_bnds.iloc[:,0])):
        if service_bnds.Artes_serv[j] == outdoor_demand_proj.ID[provider]:
            service_bnds.growth_tot_demand[j] = total_demand_growth 
            service_bnds.growth_out_demand[j] = outdoor_demand_growth
            service_bnds.perc_growth_tot_demand[j] = percent_total_demand_growth 
            service_bnds.perc_growth_out_demand[j] = percent_outdoor_demand_growth
            service_bnds.init_AW_LC[j] = initial_weighted_LC 
            service_bnds.final_AW_LC[j] = final_weighted_LC 
            service_bnds.pop_growth[j] = pop_growth
            service_bnds.init_perc_outdoor[j] = outdoor_demand_proj.iloc[provider,2]/( outdoor_demand_proj.iloc[provider,2] +  indoor_demand_proj.iloc[provider,2])
            service_bnds.final_perc_outdoor[j] =  outdoor_demand_proj.iloc[provider,11]/( outdoor_demand_proj.iloc[provider,11] +  indoor_demand_proj.iloc[provider,11])
            service_bnds.per_capita_initial[j] = per_capita_initial
            service_bnds.per_capita_final[j] = per_capita_final 
            
            break  

# Initial % Outdoor demand
fig, ax = plt.subplots(nrows=1, ncols=1, figsize = (10,10))
service_bnds.plot(column = 100 * service_bnds.init_perc_outdoor, 
                  cmap = 'YlGn', vmin = 20, vmax = 60, edgecolor = 'black', legend = True, legend_kwds={'label': "2020 % Outdoor Demand",
                        'orientation': "horizontal"})


# Pop growth 
fig, ax = plt.subplots(nrows=1, ncols=1, figsize = (10,10))
service_bnds.plot(column = 100 * service_bnds.pop_growth, 
                  cmap = 'Oranges_r', vmin = -40, vmax = 0, edgecolor = 'black', legend = True, legend_kwds={'label': "% Population Growth",
                        'orientation': "horizontal"})

# Demand growth 
fig, ax = plt.subplots(nrows=1, ncols=1, figsize = (10,10))
service_bnds.plot(column = 100 * service_bnds.perc_growth_tot_demand, 
                  cmap = 'YlOrBr', vmin = 10, vmax = 60, edgecolor = 'black', legend = True, legend_kwds={'label': "% change Demand",
                        'orientation': "horizontal"})


fig, ax = plt.subplots(nrows=1, ncols=1, figsize = (10,10))
service_bnds.plot(column = 100*service_bnds.perc_growth_out_demand, 
                  cmap = 'Blues_r', vmin = -40,  vmax = 0, edgecolor = 'black', legend = True, legend_kwds={'label': "% change Outdoor Demand",
                        'orientation': "horizontal"})

# Weighted LC 
fig, ax = plt.subplots(nrows=1, ncols=1, figsize = (10,10))
service_bnds.plot(column = service_bnds.init_AW_LC, 
                  cmap = 'viridis', vmin = 22,  vmax = 23.5, edgecolor = 'black', legend = True, legend_kwds={'label': "Initial Weighted LC",
                        'orientation': "horizontal"})

fig, ax = plt.subplots(nrows=1, ncols=1, figsize = (10,10))
service_bnds.plot(column = service_bnds.final_AW_LC, 
                  cmap = 'viridis', vmin = 22,  vmax = 23.5, edgecolor = 'black', legend = True, legend_kwds={'label': "Final Weighted LC",
                        'orientation': "horizontal"})

# Per Capita Demand
fig, ax = plt.subplots(nrows=1, ncols=1, figsize = (10,10))
service_bnds.plot(column = service_bnds.per_capita_initial*325851/365, 
                  cmap = 'Greys', vmin = 50,  vmax = 250, edgecolor = 'black', legend = True, legend_kwds={'label': "per_capita_initial",
                        'orientation': "horizontal"})

fig, ax = plt.subplots(nrows=1, ncols=1, figsize = (10,10))
service_bnds.plot(column = 100*(service_bnds.per_capita_final*325851/365 - service_bnds.per_capita_initial*325851/365)/(service_bnds.per_capita_initial*325851/365), 
                  cmap = 'bwr', vmin = -40,  vmax = 40, edgecolor = 'black', legend = True, legend_kwds={'label': "% change in per_capita_final",
                        'orientation': "horizontal"})

fig, ax = plt.subplots(nrows=1, ncols=1, figsize = (10,10))
service_bnds.plot(column = service_bnds.per_capita_final*325851/365, 
                  cmap = 'YlGnBu', vmin = 0,  vmax = 250, edgecolor = 'black', legend = True, legend_kwds={'label': "per_capita_final",
                        'orientation': "horizontal"})
