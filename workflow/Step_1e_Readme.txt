Python script 'Demand_data_processing.py' generates monthly average water demand for water providers within the study region. 
The input data is the California Water Resources Control Board monthly water provider supply data (Input Data Reference 3). 
The data is in 'Artes_node_monthly_delivery_data_CA_database.csv'
The script outputs recent (2017-2021) monthly average water demand for water providers in the file `Provider_historical_demands.csv'.
Each provider ('ID' column) has Outdoor and Indoor demand estimates that are output for use in a water model of the region. For this 
work the Indoor and Outoor values are summed and used as total monthly demands in Step 4 (Water demand projections), which
estimates indoor and outdoor components of demand using the land cover and population data. 