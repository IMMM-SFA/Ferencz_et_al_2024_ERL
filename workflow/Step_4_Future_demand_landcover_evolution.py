# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import os 
import matplotlib.pyplot as plt

#%% 

SSP = "SSP5" # change to 'SSP3' or 'SSP5'  
scenario = "med" # change to "low" , "med", or "hi"

# Create master dataframes to store projected demands for all providers. These empty 
# dataframes will be iteratively appended by the provider-specific water demand
# projection dataframes.

os.chdir("") # Path to Step 4 Folder 

columns = ['ID', '2010','2020','2030','2040','2050','2060','2070','2080','2090','2100', 'Initial_Weighted_LC', 'Final_Weighted_LC']
master_indoor_future_annual = pd.DataFrame(columns = columns)
master_indoor_future_monthly = pd.DataFrame(columns = columns)

master_indoor_future_annual_target = pd.DataFrame(columns = columns)
master_indoor_future_monthly_target = pd.DataFrame(columns = columns)
 
master_outdoor_future_annual = pd.DataFrame(columns = columns)
master_outdoor_future_monthly = pd.DataFrame(columns = columns)

historical_use_master = pd.DataFrame(columns = ['ID','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep', 'Oct', 'Nov', 'Dec'])

#master_demand_sensitivity_2100_attributes = pd.DataFrame(columns = ['ID', 'Weighted_LC', 'Urban_Area',  'Population', 'Indoor_Per_Capita', 'Outdoor_unit_area_demand', 'Green_Area'])
 
monthly_irrigation_depths = pd.DataFrame(columns = ['ID', 'Green_Frac', 'Grass_Frac', 'Tree_Frac', 'Shrub_Frac', 'Unit_area_demand', 'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep', 'Oct', 'Nov', 'Dec'])

# Provider historical population 
pop_historical = pd.read_csv("Provider_historical_population.csv")

# Historic NLCD 
NLCD_historic = pd.read_csv("NLCD_LC_areas_historic.csv")

# Artes baseline historical monthly demand data 
monthly_use_data = pd.read_csv('Provider_historical_demands.csv', index_col = 0) 

root_ids = []
for i in range(len(monthly_use_data.iloc[:,0])):
    id_len =  len(monthly_use_data.ID[i])
    
    if monthly_use_data.ID[i][id_len-7:] == '_INDOOR':
        root_ids.append(monthly_use_data.ID[i][:-7])
    
    elif monthly_use_data.ID[i][id_len-8:] == '_OUTDOOR':
        root_ids.append(monthly_use_data.ID[i][:-8])
        
    else:
        root_ids.append('NA')
        
monthly_use_data['Root_id'] = root_ids 

# Future service region urban landclass evolution (2010-2100)
LU_SSP_df = pd.read_csv(SSP+'_Aggregated_landclass_projection_data.csv', index_col = 0)
LU_SSP_ids = LU_SSP_df.Provider_ID.unique()
LU_SSP_ids = np.append(LU_SSP_ids, ['IOU_PWC','IOU_SWS_WLM']) # add root ids for two providers with multiple discrete footprints

for i in range(len(LU_SSP_df.iloc[:,0])):
    if LU_SSP_df.Provider_ID[i][0:7] == 'IOU_PWC':
        LU_SSP_df.Provider_ID[i] = 'IOU_PWC'
    elif LU_SSP_df.Provider_ID[i][0:11] == 'IOU_SWS_WLM':
        LU_SSP_df.Provider_ID[i] = 'IOU_SWS_WLM'
    else:
        continue 
    
# Future service region population from 1 km^2 Zorgein and O'neil updated 2020 - 2100 projections  
pop_ssp = pd.read_csv('service_region_population_' + SSP +'_2010_2100.csv', index_col = 0) # choose SSP3 or SSP5

# Service region landcover -> NLCD urban landclass data 
landcover_fraction_by_NLCD_LC = pd.read_csv('landcover_fraction_providers.csv')


#%% Water demand projection code block 

# Provider regions
providers = monthly_use_data.Root_id.unique() 
providers_with_LU_data = [] # a check to see how many regions use the LULC data 
outdoor_use_fraction = []
per_capita_indoor = {}
baseline_indoor_monthly = []
provider_ids = []

# Iterate over all provider regions in 'providers' array
for n in range(len(providers)):
    provider = providers[n] #
    
    landclass_fractions = landcover_fraction_by_NLCD_LC.where(landcover_fraction_by_NLCD_LC.iloc[:,0] == provider).dropna()

    # Load provider region water use data (selected using service region ID)
    hist_provider_monthly_use = monthly_use_data.where(monthly_use_data.Root_id == provider).dropna()
    
        
    monthly_use = np.sum(hist_provider_monthly_use.iloc[:,2:14], axis = 0) # sum indoor and outdoor rows
    
    
    # Create dataframes to store future demand results and provider metrics 
    columns = ['2010','2020','2030','2040','2050','2060','2070','2080','2090','2100']
    months = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
    indoor_future_annual = pd.DataFrame(data = np.zeros((1,10)), columns = columns, index = ['Indoor'])
    indoor_future_monthly = pd.DataFrame(data = np.zeros((12,10)), columns = columns, index = months)
    
    indoor_future_annual_target = pd.DataFrame(data = np.zeros((1,10)), columns = columns, index = ['Indoor'])
    indoor_future_monthly_target = pd.DataFrame(data = np.zeros((12,10)), columns = columns, index = months)
     
    outdoor_future_annual = pd.DataFrame(data = np.zeros((1,10)), columns = columns, index = ['Outdoor'])
    outdoor_future_monthly = pd.DataFrame(data = np.zeros((12,10)), columns = columns, index = months)
    
    #demand_sensitivity_2100_attributes = pd.DataFrame(data = np.array([['A', 0, 0, 0, 0, 0, 0]]), columns = ['ID', 'Weighted_LC', 'Urban_Area',  'Population', 'Indoor_Per_Capita', 'Outdoor_unit_area_demand', 'Green_Area'])

    monthly_irr_depths = pd.DataFrame(data = np.zeros((1,12)), columns = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep', 'Oct', 'Nov', 'Dec'])

    
    if provider in LU_SSP_ids and landclass_fractions.size > 0: # if provider region boundary is known and LC data is available 
                                                                   # (there are ~10 small ones/private regions that are not in CA database)
        historical_use_data = np.zeros((1,12))
        historical_use_data[:] = monthly_use.values       
        historical_use_df = pd.DataFrame(data = historical_use_data, columns = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep', 'Oct', 'Nov', 'Dec'])
        historical_use_df.insert(0,'ID', provider)      
                                        
        historical_use_master = pd.concat([historical_use_master, historical_use_df])
                                                               
        #providers_with_LU_data.append([provider])
        
        filtered_SSP = LU_SSP_df.copy()
        filtered_SSP = filtered_SSP.where(filtered_SSP.Provider_ID == provider)
        filtered_SSP = filtered_SSP.where(filtered_SSP.scenario == scenario)
        filtered_SSP = filtered_SSP.dropna()
        filtered_SSP_21 = filtered_SSP.copy()
        filtered_SSP_21 = filtered_SSP_21.where(filtered_SSP_21.urban_class == 21)
        filtered_SSP_21 = filtered_SSP_21.dropna()
        filtered_SSP_22 = filtered_SSP.copy()
        filtered_SSP_22 = filtered_SSP_22.where(filtered_SSP_22.urban_class == 22)
        filtered_SSP_22 = filtered_SSP_22.dropna()
        filtered_SSP_23 = filtered_SSP.copy()
        filtered_SSP_23 = filtered_SSP_23.where(filtered_SSP_23.urban_class == 23)
        filtered_SSP_23 = filtered_SSP_23.dropna()
        filtered_SSP_24 = filtered_SSP.copy()
        filtered_SSP_24 = filtered_SSP_24.where(filtered_SSP_24.urban_class == 24)
        filtered_SSP_24 = filtered_SSP_24.dropna()
        
        index = ['LC_21','LC_22','LC_23','LC_24']
        columns = ['2010','2020','2030','2040','2050','2060','2070','2080','2090','2100']
        data = np.zeros((4,10))
        LC_df = pd.DataFrame(data = data.copy(), index = index, columns = columns)
        
        LC_df.iloc[0,:] = np.sum(filtered_SSP_21.iloc[:, 5:])
        LC_df.iloc[1,:] = np.sum(filtered_SSP_22.iloc[:, 5:])
        LC_df.iloc[2,:] = np.sum(filtered_SSP_23.iloc[:, 5:])
        LC_df.iloc[3,:] = np.sum(filtered_SSP_24.iloc[:, 5:])
        
        
        initial_weighted_LC = (21 * LC_df.iloc[0,0] + 22 * LC_df.iloc[1,0] + 23 * LC_df.iloc[2,0] + 24 * LC_df.iloc[3,0])/np.sum(LC_df.iloc[:,0])
        final_weighted_LC = (21 * LC_df.iloc[0,-1] + 22 * LC_df.iloc[1,-1] + 23 * LC_df.iloc[2,-1] + 24 * LC_df.iloc[3,-1])/np.sum(LC_df.iloc[:,-1])
        final_urban_area = np.sum(LC_df.iloc[:,-1]) * 900/10**6 # convert pixel counts to area in km^2
        
        #demand_sensitivity_2100_attributes.ID = provider
        #demand_sensitivity_2100_attributes.Weighted_LC = final_weighted_LC
        #demand_sensitivity_2100_attributes.Urban_Area = final_urban_area
        
        # Future population
        # Load provider region population from pop_ssp 
        pop = pop_ssp.where(pop_ssp.Service_region == provider).dropna()
        pop = pop.iloc[0, 1:].values # convert to array 
        #demand_sensitivity_2100_attributes.Population = pop[9]
        
        # Historical urban landclass - green fraction data 
        green_fractions = [1 *landclass_fractions.iloc[0,1]+ landclass_fractions.iloc[0,2] + landclass_fractions.iloc[0,3], 
                            1 * landclass_fractions.iloc[0,5]+ landclass_fractions.iloc[0,6] + landclass_fractions.iloc[0,7], 
                            1 * landclass_fractions.iloc[0,9]+ landclass_fractions.iloc[0,10] + landclass_fractions.iloc[0,11],
                            1 * landclass_fractions.iloc[0,13]+ landclass_fractions.iloc[0,14] + landclass_fractions.iloc[0,15]] 
                                    
        ###### Calculate demand projection metrics 
        
        # Historical population 
        pop_hist = 0 # historical population used to calculate per capita indoor use
        
        if provider in pop_historical.Artes_ID[:].values:
            
            pop_filter = pop_historical.copy()
            pop_filter = pop_filter.where(pop_filter.Artes_ID[:] == provider).dropna(subset = 'Artes_ID')
            pop_hist = pop_filter.iloc[0,1]
            
        else: # use mean of SSP5 and SSP5 in 2020 
            pop_hist = pop[0]
        
        # Historical green area 
        total_area = 0
        outdoor_area = 0
        outdoor_grass = 0 
        outdoor_tree = 0 
        outdoor_shrub = 0 
        grass_indx = [2,6,10,14]
        tree_indx =  [1,5,9,13]
        shrub_indx = [3,7,11,15]
        
        # Instead of using the LC_df, always use the historical NLCD dataset 
        # to ensure that the SAME outdoor demand per unit green area is used for all scenarios.
        
        historic_provider_NLCD = NLCD_historic.where(NLCD_historic.iloc[:,0] == provider)
        historic_provider_NLCD = historic_provider_NLCD.dropna()
        provider_ids.append(historic_provider_NLCD.Service_region.values[0])
        
        for i in range(4):
            total_area += historic_provider_NLCD.iloc[0,i+1] * 900/10**6 # area in km^2, converted from pixel counts. Conversion is 1 pixel = 30 m x 30 m (900), and then divide by 10^6 m^2/km^2
            outdoor_area += historic_provider_NLCD.iloc[0,i+1] * green_fractions[i] * 900/10**6 # area in km^2, converted from pixel counts 
            outdoor_grass += historic_provider_NLCD.iloc[0,i+1] * landclass_fractions.iloc[0,grass_indx[i]] * 900/10**6
            outdoor_tree += historic_provider_NLCD.iloc[0,i+1] * landclass_fractions.iloc[0,tree_indx[i]] * 900/10**6
            outdoor_shrub += historic_provider_NLCD.iloc[0,i+1] * landclass_fractions.iloc[0,shrub_indx[i]]* 900/10**6
        
        initial_outdoor_area = outdoor_area # outdoor area = green area 
        service_region_green_fraction = outdoor_area/total_area
        
        # Water use in minimum month
        hist_min_month = min(monthly_use)
        
        # Outdoor demand estimate using 2.5 cm (1") irr depth in minimum use month
        outdoor_min_month = (1/12) * outdoor_area * 247.1 # units of acre-ft (conversion is 247.1 acres = 1 km^2)
        
        # Historical indoor use 
        min_month_indoor_frac = (1 - outdoor_min_month/hist_min_month) 
        indoor_hist = hist_min_month * min_month_indoor_frac # monthly indoor use acft/month
        baseline_indoor_monthly.append(indoor_hist) 
        indoor_hist_per_capita = indoor_hist/pop_hist # acft/month
        indoor_hist_per_capita_gpd = 325851 * 1/30 * indoor_hist_per_capita # gallons/day
        #demand_sensitivity_2100_attributes.Indoor_Per_Capita = indoor_hist_per_capita_gpd
        per_capita_indoor[provider] = indoor_hist_per_capita_gpd
        
        # Historical outdoor use 
        outdoor_hist = monthly_use - indoor_hist 
        
        # Annual % outdoor use 
        annual_outdoor_use_fraction = np.sum(outdoor_hist)/np.sum(monthly_use)
        outdoor_use_fraction.append(annual_outdoor_use_fraction)
        
        # Green fraction unit area monthly demand 
        monthly_green_space_unit_demand = outdoor_hist/outdoor_area # acft/month/km^2 of greenspace 
        #demand_sensitivity_2100_attributes.Outdoor_unit_area_demand =  sum(monthly_green_space_unit_demand.values)
        
        # Estimated monthly irrigation depths from historical use + Landcover data 
        monthly_irr_depths.iloc[0,:] = 12*monthly_green_space_unit_demand.values/247 # units: monthly_green_space_unit_demand (acft/km^2)/(247 acres/km^2) = ft/month * 12 inches/foot
        
        ###### Generate Future demand projections
    
        # Step 1: Indoor demand projection 
        
        # Baseline (2020) per capita indoor demand 
        for i in range(10):
            indoor_future_annual.iloc[0,i] = pop[i] * indoor_hist_per_capita * 12 
            indoor_future_monthly.iloc[:,i] = pop[i] * indoor_hist_per_capita
            
        # Step 2: Outdoor demand projection
        future_outdoor_area = np.zeros(10) 
        for i in range(10):
            outdoor_area = 0
            for j in range(4):
                outdoor_area += LC_df.iloc[j,i] * green_fractions[j] * 900/10**6 # area in km^2, converted from pixel counts 
            
            future_outdoor_area[i] = outdoor_area
            
            # if i == 9:
            #     demand_sensitivity_2100_attributes.Green_Area = outdoor_area
        
        for i in range(10):
            outdoor_future_monthly.iloc[:,i] = future_outdoor_area[i] * monthly_green_space_unit_demand.values
            outdoor_future_annual.iloc[0,i] = np.sum(outdoor_future_monthly.iloc[:,i])
    
    # skip providers without defined boundaries and no LU or landcover data 

    else:
        continue 
    
    
    # Save results for provider 
    indoor_future_annual.insert(0, 'ID', provider)
    indoor_future_annual.insert(11, 'Initial_Weighted_LC', initial_weighted_LC)
    indoor_future_annual.insert(12, 'Final_Weighted_LC', final_weighted_LC)
    indoor_future_monthly.insert(0, 'ID', np.tile(provider, 12))

    outdoor_future_annual.insert(0, 'ID', provider)
    outdoor_future_annual.insert(11, 'Initial_Weighted_LC', initial_weighted_LC)
    outdoor_future_annual.insert(12, 'Final_Weighted_LC', final_weighted_LC)
    outdoor_future_monthly.insert(0, 'ID', np.tile(provider, 12))
    
    monthly_irr_depths.insert(0, 'ID', provider)
    monthly_irr_depths.insert(1, 'Green_Frac', service_region_green_fraction)
    monthly_irr_depths.insert(2, 'Grass_Frac', outdoor_grass/initial_outdoor_area)
    monthly_irr_depths.insert(3, 'Tree_Frac', outdoor_tree/initial_outdoor_area)
    monthly_irr_depths.insert(4, 'Shrub_Frac', outdoor_shrub/initial_outdoor_area)
    monthly_irr_depths.insert(5, 'Unit_area_demand', np.sum(monthly_green_space_unit_demand))
    
    # Append to provider results to master dataframes 
    master_indoor_future_annual = pd.concat([master_indoor_future_annual, indoor_future_annual])
    master_indoor_future_monthly = pd.concat([master_indoor_future_monthly, indoor_future_monthly])

    master_outdoor_future_annual = pd.concat([master_outdoor_future_annual, outdoor_future_annual])
    master_outdoor_future_monthly = pd.concat([master_outdoor_future_monthly, outdoor_future_monthly])
    
    monthly_irrigation_depths = pd.concat([monthly_irrigation_depths, monthly_irr_depths])
    
    #master_demand_sensitivity_2100_attributes = pd.concat([master_demand_sensitivity_2100_attributes, demand_sensitivity_2100_attributes])
    
# Save outputs as CVSs 
master_outdoor_future_annual = master_outdoor_future_annual.copy()
master_indoor_future_annual = master_indoor_future_annual.copy()

indoor_baseline = pd.DataFrame(data = baseline_indoor_monthly, index = provider_ids)
indoor_baseline.to_csv("indoor_baseline.csv")

#master_demand_sensitivity_2100_attributes.to_csv("demand_sensitivity_2100_attributes_" + SSP + "_" + scenario + ".csv", index = False) # uncomment to output demand sensitivity csv used for Figure 8 
master_indoor_future_annual.to_csv('Provider_projection_indoor_' + SSP + '_' + scenario + '.csv')
master_outdoor_future_annual.to_csv('Provider_projection_outdoor_' + SSP + '_' + scenario + '.csv')
master_indoor_future_monthly.to_csv('Provider_projection_indoor_monthly_' + SSP + '_' + scenario + '.csv')
master_outdoor_future_monthly.to_csv('Provider_projection_outdoor_monthly_' + SSP + '_' + scenario + '.csv')
monthly_irrigation_depths.to_csv('Provider_outdoor_properties_.csv') # only needs to be output once 
historical_use_master.to_csv('Historical_use_master.csv') # only needs to be output once 
