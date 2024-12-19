Python script Future_demand_landcover_evolution.py generates future decadal demand projections using unit dempand factors based on average monthly water supply over 2017-2021 from Step 1e. Set SSP (3 or 5) and zoning scenario (low, med, hi) in Lines 10-11 of script. Script will output indoor and outdoor demands for each provider and also landcover and irrigation depth estimates. Run for SSP5 low, SSP5 med, SSP5 hi, and SSP3 med. Outputs are used by the plotting scripts associated with Figures 4 through 8 of the paper. To generate outputs used for Figire 8, uncomment lines associated with demand_sensitivity_2100_attributes or master_demand_sensitivity_2100_attributes

Python script Future_demand_landcover_evolution_min_and_max_scenarios.py generates future decadal demand projections used on unit demand factors based on minimum and maximum monthly water supply factors over 2014-2021 from Step 1e. Script will output minimum and maximum indoor and outdoor demand projections for each provider and also landcover and irrigation depth estimates. Run for SSP5 low, SSP5 med, SSP5 hi, and SSP3 med by modifying Lines 10-11 of script and specific whether to use the minimum or maximum demand factors by modifying Line 42 to set min or max. Outputs are used by the plotting scripts associated with Figures 4 and 5.

Outputs for each SSP (3 or 5) and zoning scenario (low, med, hi) and min, max, or recent average. All volumes in acre-feet:
-Annual indoor demand 
-Annual outdoor demand
-Monthly indoor demand. First column is months (1-12). 
-Monthly outdoor demand. First column is months (1-12). 
-Provider outdoor properties (the same for all cases, only needs to be output once)
-Provider historical demands (the same for all cases, only needs to be output once)
-Demand sensitivity metrics used for the analysis in Figure 8 (only needs to be output for the average scenarios as these are only considered for Figure 8)
-Reformatted monthly demands used for Figures 4 and 5. These have the format Indoor(or Outdoor)_YYYY_SSPX_zoningScenario (e.g., Indoor_2100_SSP3_med) for the average 
monthly demand scenario and Indoor(or Outdoor)_2100_SSPX_demandScenario_zoningScenario_pop for the min and max demand scenarios (e.g., Indoor_2010_SSP5_min_med_with_pop)
