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
1. **NLCD Historical**. Multi-Resolution Land Characteristics Consortium. https://www.mrlc.gov/viewer/. Accessed 10/2/23
2. **Hi res land cover**. Coleman, Red Willow (2020), “Southern California 60-cm Urban Land Cover Classification ”, Mendeley Data, V1, doi: 10.17632/zykyrtg36g.1
3. **Monthly water provider data**. California State Water Resources Control Board. Water Conservation and Production Reports. https://www.waterboards.ca.gov/water_issues/programs/conservation_portal/conservation_reporting.html accessed 6/2/23
4. **Annual sectoral water provider data**.  California State Water Resources Control Board. DWR Urban Water Use Objective Analyzer Tool. https://lab.data.ca.gov/dataset/dwr-urban-water-use-objective-analyzer-tool accessed 6/2/23
5. **Water provider boundaries**. California State Water Resources Control Board. Service area boundaries of drinking water service providers, as verified by the Division of Drinking Water. https://gispublic.waterboards.ca.gov/portal/home/item.html?id=fbba842bf134497c9d611ad506ec48cc accessed 6/2/23
6. **Population projections**. Zoraghein, H., & O'Neill, B. (2020). Data Supplement: U.S. state-level projections of the spatial distribution of population consistent with Shared Socioeconomic Pathways. (v0.1.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.3756179
7. **Urban growth model projections**. McManamay, R., & Vernon, C. (2023). High-resolution (30-m) urban land cover projections for Los Angeles California Urban Area: 2010 to 2100 under SSP5 (Version v1) [Data set]. MSD-LIVE Data Repository. https://doi.org/10.57931/19088234 

### Output Data 
8. MSD Live Ferencz and Capone data processing and demand projections (2024)

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

- Use the QGIS model builder function to process the hi-resolution landcover data **Input Data [2]**. Inputs are the NLCD recent historical land classification raster (**Input Data [1]**), the hi-resolution landcover raster from **Input Data [2]**, and the provider boundaries (**Input Data [5]**. Outputs are four `.tiff` rasters for each water provider region (or sub-region), one for each NLCD urban land class. All of the clipped rasters are saved on MSD Live (**Code Reference [9]**). This processs is very time consuming so we provide the output rasters. The naming convention is `PROVIDER_NAME_LC##.tiff` where ## denotes the NLCD land classification (21, 22, 23, 24).

**1e** Calculate recent average monthly water demand for each water provider:
- Download monthly water data by water provider for all of California (**Input Data [3]**).
- Filter out providers that are outside of the study area (done manually).
- Python script `Demand_data_processing.py` converts monthly demand to common units (acre-feet, 1 acre-foot = 1,233 m<sup>3</sup> and then calculates average monthly demands for each water provider. The output is `Provider_historical_demands.csv`. 

**2**. Derive NLCD urban land classification -- landcover relationships for each water provider region:
- Two Python scripts are used to process all of the clipped landcover data produced in **Step 1d**. These scripts are located in **Code Reference [9]**: `Data_Processing_Urban_LC_green_fraction_by_service_region_Batch_1` and `Data_Processing_Urban_LC_green_fraction_by_service_region_Batch_2`. The outputs are three sets of `.csv` files for each Batch. `landclass_area_providers.csv`, `landcover_area_providers.csv`, and `landcover_fraction_providers.csv`. The Batch 2 script combines the outputs into single `.csv` files.  

**3**. Analyze pixel-level urban intensification and extensification  
- Use Python script `Urban_growth_change_mapping.py`. Inputs are initial and final urban morphology rasters. Outputs are 
- Visualize in QGIS....

**4** Generate future demand projections:
- Python script `Future_demand_landcover_evolution.py`. Set SSP (3 or 5) and zoning scenario (low, med, hi) in Lines `10-11` of script. Script will output indoor and outdoor demands for each provider and also landcover and irrigation depth estimates. Run for SSP5 low, SSP5 med, SSP5 hi, and SSP3 med for a total of 12 `csv` files. These outputs are used by the plotting scripts associated with Figures 4 through 7 of the paper.

## Reproduce my Figures 

- Figure 1. Subplots a, b, d, e, f made in QGIS using **Input Data [1][2][5]** and touched up using Inkscape. Subplut c plotted from `Figure_1.py`. 
- Figure 2. Wire diagram made in Powerpoint. Subplots b and c `Figure_2.py`. Subplot d in QGIS using **Input Data [7]**.  
- Figure 3. Output `tiff` files from **Step 3** visualized in QGIS. 
- Figure 4. Outputs from **Step 4** and **Step 1c**. `Figure_4.py`. 
- Figure 5. Outputs from **Step 4** and **Step 1c**. `Figure 5.py`.
- Figure 6. Outputs from **Step 4**. `Figure_6.py`. 
- Figure 7. Outputs from **Step 4**. `Figure_7.py`. 
