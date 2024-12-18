# -*- coding: utf-8 -*-
"""
"""

import pandas as pd
import numpy as np 
import math 
import os 
import matplotlib.pyplot as plt

#%% Import datasets 

os.chdir("C:/Users/fere556/OneDrive - PNNL/Documents/Artes/Demand_paper/Paper_Figures/Figure_8_Demand_Sensitivity")

SSP = 5 # choose SSP3 or SSP5
intensification = 'hi' # choose low, med, or hi

# Load corresponding results 

### Values that vary by SSP and intensification scenario 
# Provider Attributes in 2100: Population, weighted LC, Indoor per capita historical, 
# Outdoor unit are demand, and urban area in 2100 

os.chdir("Figure 8")
provider_attributes_2100 = pd.read_csv("demand_sensitivity_2100_attributes_SSP" + str(SSP) + "_" + intensification + ".csv")
provider_attributes_2100 = provider_attributes_2100.dropna()
provider_attributes_2100 = provider_attributes_2100.reset_index(drop = True)
#provider_attributes_2100_low = provider_attributes_2100.reset_index(drop = True)

# Estimated indoor household per capita demand - from CA provider sectoral use data
historical_hh_indoor = pd.read_csv("Provider_historical_household_indoor.csv")


#%% Make DataFrame to store 2100 values 

## Demand sensitivity results dataframe
# rows = Provider IDs 
columns = ['ID', 'Baseline', 'Baseline_household_eff', 'Baseline_outdoor_high', 
           'Baseline_outdoor_low', 'Baseline_outdoor_high_household_eff', 
           'Baseline_outdoor_low_household_eff', 'Baseline_outdoor_high_climate', 
           'Baseline_outdoor_low_household_eff_climate', 'Baseline_climate', 'Flag_hist_res_indoor']

demand_sensitivity_master = pd.DataFrame(columns = columns)


#%% Parameters controlling future water demand

# 1) per capita household indoor - lower limit

indoor_household_per_capita_lower = 42 # this is in gpcpd

# climate factor - draw from RAND and Pacific Institute, find other values in literature

climate_factors = [1.16]

# Upper and lower bounds for Weighted LC vs green fraction 
# regression equations to define the upper and lower bounds 
# reg_upper = 4.94 - 0.2003 * Weighted_LC 
# reg_lower = 4.29 - 0.179 * Weighte_LC 

# Upper and lower bounds for Weighted LC vs unit area outdoor demand 
# piecewise function for upper and lower bounds based on weighted LC 
upper_unit_area = 900 # acft/km^2
lower_unit_area = 300  # actt/km^2


#%% Analysis for all providers- THIS DOES NOT NEED TO BE DONE TO PLOT THE RESULTS IN FIGURE 8 
#   That can be done with code block below. The demand sensivity projections are included here 
#   for reproducibility. 

for n in range(len(provider_attributes_2100.iloc[:,0])):
    demand_sensitivity = pd.DataFrame(data = [['A',0,0,0,0,0,0,0,0,0,0]], columns = columns)
    provider = provider_attributes_2100.ID[n]
    demand_sensitivity.ID = provider_attributes_2100.ID[n]
    
    # Indoor use 
    # First check if historical hh indoor is available 
    if provider in historical_hh_indoor.Artes_ID.values:
        demand_sensitivity.Flag_hist_res_indoor[0] = 1
        hh_indoor = historical_hh_indoor.where(historical_hh_indoor.Artes_ID == provider).dropna()
        household_indoor = 0 
        if hh_indoor.iloc[0,1] > indoor_household_per_capita_lower:
            household_indoor = indoor_household_per_capita_lower
        else:
            household_indoor = hh_indoor.iloc[0,1]
    
        other_indoor = provider_attributes_2100.Indoor_Per_Capita[n] - hh_indoor.iloc[0,1]
        
        # 2100 Indoor baseline and w/hh conservation: acft/month 
        indoor_household_eff = provider_attributes_2100.Population[n] * (household_indoor + other_indoor) * (30/325851)
        indoor_baseline = provider_attributes_2100.Population[n] * (hh_indoor.iloc[0,1] + other_indoor) * (30/325851)
    
    
    # If historical hh indoor not available, calc 2100 demand:acft/month
    else:
        indoor_household_eff = provider_attributes_2100.Population[n] * (provider_attributes_2100.Indoor_Per_Capita[n]) * (30/325851)
        indoor_baseline = provider_attributes_2100.Population[n] * (provider_attributes_2100.Indoor_Per_Capita[n]) * (30/325851)
        
    # Outdoor use     
    
    # Green area (km^2)
    baseline_green_area = provider_attributes_2100.Green_Area[n]
    green_area_high = (4.94 - 0.2003 * provider_attributes_2100.Weighted_LC[n]) * provider_attributes_2100.Urban_Area[n]
    green_area_low =  (4.29 - 0.179 * provider_attributes_2100.Weighted_LC[n]) * provider_attributes_2100.Urban_Area[n]
    
    #provider_attributes_2100.Outdoor_unit_area_demand[n] # acft/yr/km^2 of green space 
    
    # Outdoor Demand: acft/yr 
    outdoor_demand_baseline = baseline_green_area * provider_attributes_2100.Outdoor_unit_area_demand[n]
    outdoor_demand_high = green_area_high * upper_unit_area
    outdoor_demand_low = green_area_low * lower_unit_area
    
    # Update fields in demand_sensitivity and append to demand_sensitivity_master
    #columns = ['ID', 'Baseline', 'Baseline_household_eff', 'Baseline_outdoor_high', 
               #'Baseline_outdoor_low', 'Baseline_outdoor_high_household_eff', 
               #'Baseline_outdoor_low_household_eff', 'Baseline_outdoor_high_climate']
    
    demand_sensitivity.Baseline = 12*indoor_baseline + outdoor_demand_baseline
    demand_sensitivity.Baseline_household_eff = 12*indoor_household_eff + outdoor_demand_baseline
    demand_sensitivity.Baseline_outdoor_high = 12*indoor_baseline + outdoor_demand_high
    demand_sensitivity.Baseline_outdoor_low = 12*indoor_baseline +  outdoor_demand_low
    demand_sensitivity.Baseline_outdoor_high_household_eff = 12*indoor_household_eff + outdoor_demand_high
    demand_sensitivity.Baseline_outdoor_low_household_eff = 12*indoor_household_eff +  outdoor_demand_low
    demand_sensitivity.Baseline_outdoor_high_climate = 12*indoor_baseline + outdoor_demand_high * climate_factors[0]
    demand_sensitivity.Baseline_outdoor_low_household_eff_climate =12* indoor_household_eff + outdoor_demand_low * climate_factors[0]
    demand_sensitivity.Baseline_climate = 12*indoor_baseline + outdoor_demand_baseline * climate_factors[0]
    demand_sensitivity_master = pd.concat([demand_sensitivity_master,  demand_sensitivity])

# Save for each SSP (SSP3 and SSP5) and intensification scenario (low, med, hi)
demand_sensitivity_master.to_csv("demand_sensitivity_2100_SSP" + str(SSP) + "_" + intensification + ".csv")


#%% Calculate % change from baseline projection 

# Figures for SSP3 and SSP5 showing sensitivity demands compared to 
# the demands from the demand projection methodology. Presented as total demand for all providers, as well as outdoor and indoor 
# components. 

filenames = ['SSP3_med', 'SSP5_low', 'SSP5_hi']

percent_change_indoor = np.zeros((67,3))
percent_change_climate = np.zeros((67,3))

# All of LAC 

for i in range(3):
    
    demand_sensitivity_master = pd.read_csv("demand_sensitivity_2100_" + filenames[i] + ".csv")
    demand_sensitivity_master = demand_sensitivity_master.where(demand_sensitivity_master.ID != 'CTY_VER') # remove outlier 
    demand_sensitivity_master = demand_sensitivity_master.where(demand_sensitivity_master.Flag_hist_res_indoor == 1).dropna()
    
    percent_change_indoor[:,i] = 100 * (demand_sensitivity_master.iloc[:,3] - demand_sensitivity_master.iloc[:,2])/demand_sensitivity_master.iloc[:,2]
    percent_change_climate[:,i] = 100 * (demand_sensitivity_master.iloc[:,10] - demand_sensitivity_master.iloc[:,2])/demand_sensitivity_master.iloc[:,2]
    

# Violin plots - Figure 8 
plt.violinplot(percent_change_indoor,
                  showmeans=False,
                  showmedians=True)


plt.xticks([1, 2, 3], ['SSP3, med', 'SSP5, low', 'SSP5, high'])

plt.violinplot(percent_change_climate,
                  showmeans=False,
                  showmedians=True)

plt.ylabel('% difference from baseline')
plt.xticks([1, 2, 3], ['SSP3', 'SSP5low', 'SSP5high'])


