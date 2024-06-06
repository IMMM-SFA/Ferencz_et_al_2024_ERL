Python script "Historical_NLCD_raster_processing.py" uses the water provider boundary shapefile data 
(Artes_service_regions_updates.shp). Artes refers to the water supply model for the LA region that 
resolves water provider regions. 

Output is the NLCD_LC_area_historic.csv. Delete first column (index values) if using for executing
other steps or plotting. The areas in the output are pixel counts. Pixels are 30 m x 30 m. 
Pixel counts are converted to areas when used in the other modeling steps. 
