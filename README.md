<!--- [![DOI](https://zenodo.org/badge/265254045.svg)](https://zenodo.org/doi/10.5281/zenodo.10442485) --->

# ferencz_et_al_2024_ERL

## Urban morphology and urban water demand evolution: A case study in the land constrained Los Angeles region 
Stephen B. Ferencz <sup>1</sup>, Jim Yoon <sup>1</sup>, Johanna Capone <sup>2</sup>, Ryan McManamay <sup>3</sup> 
1. Pacific Northwest National Laboratory, Richland, WA, USA
2. Virginia Tech, Blacksburg, VA
3. Baylor University, Waco, TX

Abstract: The interactions between population growth, urban morphology, and water demand have important implications for water resources and supply in urban regions. Outdoor water use for irrigation comprises a significant fraction of urban water demand, which is potentially influenced by long-term changes in urban morphology. To investigate this, we used spatially explicit projections of urban land development intensity (fraction impervious area) generated from a 30-m resolution urban growth model for the Los Angeles region. Recent historical data on water use and high resolution landcover data were used to establish relationships between green area, urban development intensity, and outdoor water demand. These relationships were then used to project outdoor and total water demand in 2100 using the urban growth model outputs. We considered two different population scenarios informed by the Shared Socioeconomic Pathway (SSP) projections for the region (SSP3 and SSP5), and three scenarios of urban development intensification. We found that water demand growth in land constrained regions like Los Angeles significantly deviated from population growth, with lower water demand growth due to shrinking of green area. Our analysis is resolved for over 80 water providers in the region, from urban core to suburban fringe, and highlights diverse demand responses influenced by initial urban form and water demand attributes. Compared to previous studies, our work is unique in coherently linking high resolution SSP population scenarios, urban land cover evolution, and urban water demand projections, demonstrating the approach for the Los Angeles region – the largest population center in the western United States. 

## Data Sources 

### Input Data 
1. NLCD Historical
2. Hi res land cover
3. Monthly water provider data
4. Annual sectoral water provider data
5. Water provider boundaries 
6. Population projections
7. Urban growth model projections 

### Output Data 
8. MSD Live Ferencz demand projections (2024)

## Code Reference 
9. MSD Live Ferencz and Capone data processing and demand projections (2024) 

## Contributing Modeling Software 
Standard Python Packages, geopandas, rasterio, ....
 
## 

## Reproduce my Experiment 

**1a**. Process the NLCD Historical Data:

- Download NLCD for study region from MLRC. **Input Data [1]**. This is `NLCD_2019_Land_Cover_L48_20210604_clNjCWtDUmB6F5woFH6g.tiff` in **Code Reference [9]**. 
- Use NLCD_processing.py to derive the urban landcover attributes for each provider boundary defined by **Input Data[5]**
- Output is `NLCD_LC_areas_historic.csv` located in **Code Reference [9]**

**1b**. Process Population Projection Data:

- Download 1 km<sup>2</sup> population projections from **Input Data [6]**
- Clip CA data to study region using QGIS. 
- Downscale to 30 m<sup>2</sup> using QGIS built in function. Save downscaled rasters as `.tiff` files. These are in **Code Reference [9]** with the format `LA_SSPX_urban_YYYY.tiff`, where X = "3" or "5" and YYYY = year (e.g. 2100).
- The Python script `Data_Processing_Urban_growth_projection_rasters.py` located in **Code Reference [9]** uses the downscaled population rasters and provider boundaries (**Input Data[5]**) to calculate the projected population within each water provider region. Output is two `.csv` files, one for each SSP scenario: `SSP3_Aggregated_landclass_projection_data.csv` and `SSP5_Aggregated_landclass_projection_data.csv`

**1c**. Process urban landcover projections:

- Download 30 m urban landcover projections from **Input Data [7]**.
- Python script `Data_Processing_Urban_growth_projection_rasters.py` aggregates the urban land projections for each water provider. The script generates four `.csv` files for each SSP and zoning scenario ("low," "medium," "high"). These are located in **Code Reference [9]**. The Python script then aggregates the SSP-specific outputs into single `.csv` files with the names: `SSP3_Aggregated_landclass_projection_data.csv` and `SSP5_Aggregated_landclass_projection_data.csv'

**1d**. Generate landcover rasters for each urban land class (21, 22, 23, 24) within each water provider boundary:

- Use the QGIS model builder function to process the hi-resolution landcover data **Input Data [2]**. Inputs are the NLCD recent historical land classification raster (**Input Data [1]**), the hi-resolution landcover raster from **Input Data [2]**, and the provider boundaries (**Input Data [5]**. Outputs are four `.tif` rasters for each water provider region (or sub-region), one for each NLCD urban land class. All of the clipped rasters are saved on MSD Live (**Code Reference [9]**). This processs is very time consuming so we provide the output rasters. The naming convention is `PROVIDER_NAME_LC##.tif` where ## denotes the NLCD land classification (21, 22, 23, 24).

**1e** Calculate recent average monthly water demand for each water provider:
- Download monthly water data by water provider for all of California (**Input Data [3]**).
- Filter out providers that are outside of the study area (done manually).
- Python script `Demand_data_processing.py` converts monthly demand to common units (acre-feet, 1 acre-foot = 1,233 m<sup>3</sup> and then calculates average monthly demands for each water provider. The output is `Provider_historical_demands.csv`. 

**2**. Derive NLCD urban land classification -- landcover relationships for each water provider region:
- Two Python scripts are used to process all of the clipped landcover data produced in **Step 1d**. These scripts are located in **Code Reference [9]**: `Data_Processing_Urban_LC_green_fraction_by_service_region_Batch_1` and `Data_Processing_Urban_LC_green_fraction_by_service_region_Batch_2`. The outputs are three sets of `.csv` files for each Batch. `landclass_area_providers.csv`, `landcover_area_providers.csv`, and `landcover_fraction_providers.csv`. The Batch 2 script combines the outputs into single `.csv` files.  

**3** 
