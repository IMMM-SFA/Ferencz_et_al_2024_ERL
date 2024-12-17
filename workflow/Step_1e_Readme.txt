Python scripts 'Demand_data_processing_2017_2021_data.py'and'Demand_data_processing_2014_2021_data.py'generate 
monthly average, minimum, and maximum water demands for each water provider within the study region. 
The input data is the California Water Resources Control Board monthly water provider supply data (Input Data Reference 3). 
The data is in 'Artes_node_monthly_delivery_data_CA_database.csv'
The script outputs recent (2017-2021) monthly average water demand for water providers in the file `Provider_historical_demands.csv' and 
minimum and maximum demands in the files 'Provider_historical_demands_min.csv' and 'Provider_historical_demands_max.csv'.
Each provider ('ID' column) has Outdoor and Indoor demand estimates that are output for use in a water model of the region. In this 
work the Indoor and Outoor values are summed and used as total monthly demands in Step 4 (Water demand projections), which
estimates indoor and outdoor components of demand using the land cover and population data and the minimum use month, as
described in the paper. 