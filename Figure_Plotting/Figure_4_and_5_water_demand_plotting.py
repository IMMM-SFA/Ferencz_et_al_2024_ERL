# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import os 
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

os.chdir("C:/Users/fere556/OneDrive - PNNL/Documents/Artes/Demand_paper/Paper_Figures/Figure_4_5_Monthly_and_Annual_Demands_in_2100")

# Historic use is from Step 1e and the version used for this is output from Step 4 
Historic_use = pd.read_csv("Historical_use_2017_2021.csv")

# These values were aggregated using the outputs from Step 4 
Projected_use = pd.read_csv("Figure_4_data_total_LA_providers.csv")

# These are demand projections from Step 4
Indoor_2100_ssp3_med = pd.read_csv("Indoor_2100_SSP3_med.csv")
Indoor_2100_ssp5_lo = pd.read_csv("Indoor_2100_SSP5_low.csv")
Indoor_2100_ssp5_med = pd.read_csv("Indoor_2100_SSP5_med.csv")
Indoor_2100_ssp5_hi = pd.read_csv("Indoor_2100_SSP5_hi.csv")

Outdoor_2100_ssp3_med = pd.read_csv("Outdoor_2100_SSP3_med.csv")
Outdoor_2100_ssp5_lo = pd.read_csv("Outdoor_2100_SSP5_low.csv")
Outdoor_2100_ssp5_med = pd.read_csv("Outdoor_2100_SSP5_med.csv")
Outdoor_2100_ssp5_hi = pd.read_csv("Outdoor_2100_SSP5_hi.csv")

#%% Figure 4: Plot LA annual and monthly total and outdoor use 

fig, axs  = plt.subplots(figsize = (8,7), nrows = 2, ncols = 2)
axs[0,0].plot(np.arange(12), Projected_use.iloc[24,3:15], color = 'black')
axs[0,0].plot(np.arange(12), Projected_use.iloc[8,3:15], color = 'green')
axs[0,0].plot(np.arange(12), Projected_use.iloc[9,3:15], linestyle = '-', color = 'blue')
axs[0,0].plot(np.arange(12), Projected_use.iloc[10,3:15], color = 'gold')
axs[0,0].plot(np.arange(12), Projected_use.iloc[11,3:15], color = 'orange')
axs[0,0].set_ylabel('Monthly Demand (acre-feet)')
axs[0,0].set_xticks([0,1,2,3,4,5,6,7,8,9,10,11], ['Jan', 'Feb','Mar','Apr', 'May', 'Jun','Jul','Aug', 'Sep','Oct','Nov', 'Dec'], rotation = 90)

axs[1,0].plot(np.arange(12), Projected_use.iloc[14,3:15], color = 'black')
axs[1,0].plot(np.arange(12), Projected_use.iloc[0,3:15], color = 'green')
axs[1,0].plot(np.arange(12), Projected_use.iloc[1,3:15], linestyle = '--', color = 'blue')
axs[1,0].plot(np.arange(12), Projected_use.iloc[2,3:15], color = 'gold')
axs[1,0].plot(np.arange(12), Projected_use.iloc[3,3:15], color = 'orange')
axs[1,0].set_ylabel('Monthly Outdoor Demand (acre-feet)')
axs[1,0].set_xticks([0,1,2,3,4,5,6,7,8,9,10,11], ['Jan', 'Feb','Mar','Apr', 'May', 'Jun','Jul','Aug', 'Sep','Oct','Nov', 'Dec'], rotation = 90)

axs[0,1].scatter(0, Projected_use.iloc[24,15], color = 'black')
axs[0,1].scatter(1, Projected_use.iloc[8,15], color = 'green')
axs[0,1].scatter(2, Projected_use.iloc[9,15], color = 'blue')
axs[0,1].scatter(3, Projected_use.iloc[10,15], color = 'gold')
axs[0,1].scatter(4, Projected_use.iloc[11,15], color = 'orange')
axs[0,1].set_ylabel('Annual Demand (acre-feet)')
axs[0,1].set_xticks([0,1,2,3,4], ['Hist', 'SSP3', 'SSP5, low', 'SSP5, med', 'SSP5, hi'], rotation = 90)

axs[1,1].scatter(0, Projected_use.iloc[15,15], color = 'black')
axs[1,1].scatter(1, Projected_use.iloc[0,15], color = 'green')
axs[1,1].scatter(2, Projected_use.iloc[1,15], color = 'blue')
axs[1,1].scatter(3, Projected_use.iloc[2,15], color = 'gold')
axs[1,1].scatter(4, Projected_use.iloc[3,15], color = 'orange')
axs[1,1].set_ylabel('Annual Outdoor Demand (acre-feet)')
axs[1,1].set_xticks([0,1,2,3,4], ['Hist', 'SSP3', 'SSP5, low', 'SSP5, med', 'SSP5, hi'], rotation = 90)

# Historical outdoor demand is reflected by the demand projection output for the
# first decade since this reflects current usage and green area within each 
# water provider 

plt.tight_layout()

#%% Figure 5: Provider-level examples of annual and monthly total and outdoor use 

# City of Compton 
fig, axs  = plt.subplots(figsize = (7,3), nrows = 1, ncols = 2)
index = 7 #27
hist_index = 7 #27
axs[0].plot(np.arange(12), Historic_use.iloc[hist_index,2:14], color = 'black')
axs[0].plot(np.arange(12), Indoor_2100_ssp3_med.iloc[index,2:14] + Outdoor_2100_ssp3_med.iloc[index,2:14], color = 'green')
axs[0].plot(np.arange(12), Indoor_2100_ssp5_lo.iloc[index,2:14] + Outdoor_2100_ssp5_lo.iloc[index,2:14], linestyle = '-', color = 'blue')
axs[0].plot(np.arange(12), Indoor_2100_ssp5_med.iloc[index,2:14] + Outdoor_2100_ssp5_med.iloc[index,2:14], color = 'gold')
axs[0].plot(np.arange(12), Indoor_2100_ssp5_hi.iloc[index,2:14] + Outdoor_2100_ssp5_hi.iloc[index,2:14], color = 'orange')
axs[0].set_xticks([0,1,2,3,4,5,6,7,8,9,10,11], ['Jan', 'Feb','Mar','Apr', 'May', 'Jun','Jul','Aug', 'Sep','Oct','Nov', 'Dec'], rotation = 90)
#axs[0,0].yaxis.set_major_locator(MultipleLocator(20))
#axs[0,0].yaxis.set_minor_locator(MultipleLocator(10))
#axs[0,0].set_ylim([60,120])
axs[0].set_ylabel('Monthly Demand (acft)')


#axs[0,1].scatter(0, np.sum(Historic_use.iloc[80,2:14])-np.sum(Historic_use.iloc[80,2:14]), color = 'black')
axs[1].scatter(1, 100*(np.sum(Indoor_2100_ssp3_med.iloc[index,2:14] + Outdoor_2100_ssp3_med.iloc[index,2:14]) -  np.sum(Historic_use.iloc[hist_index,2:14]))/np.sum(Historic_use.iloc[hist_index,2:14]), color = 'green')
axs[1].scatter(2, 100*(np.sum(Indoor_2100_ssp5_lo.iloc[index,2:14] + Outdoor_2100_ssp5_lo.iloc[index,2:14]) - np.sum(Historic_use.iloc[hist_index,2:14]))/np.sum(Historic_use.iloc[hist_index,2:14]), color = 'blue')
axs[1].scatter(3, 100*(np.sum(Indoor_2100_ssp5_med.iloc[index,2:14] + Outdoor_2100_ssp5_med.iloc[index,2:14]) - np.sum(Historic_use.iloc[hist_index,2:14]))/np.sum(Historic_use.iloc[hist_index,2:14]), color = 'gold')
axs[1].scatter(4, 100*(np.sum(Indoor_2100_ssp5_hi.iloc[index,2:14] + Outdoor_2100_ssp5_hi.iloc[index,2:14]) - np.sum(Historic_use.iloc[hist_index,2:14]))/np.sum(Historic_use.iloc[hist_index,2:14]), color = 'orange')
axs[1].set_xticks([1,2,3,4], ['SSP3', 'SSP5, low', 'SSP5, med', 'SSP5, hi'], rotation = 90)
#axs[0,1].yaxis.set_major_locator(MultipleLocator(10))
#axs[0,1].yaxis.set_minor_locator(MultipleLocator(5))
#axs[0,1].set_ylim([-10,40])
axs[1].set_ylabel('% change')

plt.tight_layout()


# Walnut Valley Water District
fig, axs  = plt.subplots(figsize = (7,3), nrows = 1, ncols = 2)
index =  47 # index in population projection outputs 
hist_index = 48 # index in historic use data 
axs[0].plot(np.arange(12), Historic_use.iloc[hist_index,2:14], color = 'black')
axs[0].plot(np.arange(12), Indoor_2100_ssp3_med.iloc[index,2:14] + Outdoor_2100_ssp3_med.iloc[index,2:14], color = 'green')
axs[0].plot(np.arange(12), Indoor_2100_ssp5_lo.iloc[index,2:14] + Outdoor_2100_ssp5_lo.iloc[index,2:14], linestyle = '-', color = 'blue')
axs[0].plot(np.arange(12), Indoor_2100_ssp5_med.iloc[index,2:14] + Outdoor_2100_ssp5_med.iloc[index,2:14], color = 'gold')
axs[0].plot(np.arange(12), Indoor_2100_ssp5_hi.iloc[index,2:14] + Outdoor_2100_ssp5_hi.iloc[index,2:14], color = 'orange')
axs[0].set_xticks([0,1,2,3,4,5,6,7,8,9,10,11], ['Jan', 'Feb','Mar','Apr', 'May', 'Jun','Jul','Aug', 'Sep','Oct','Nov', 'Dec'], rotation = 90)
#axs[0,0].yaxis.set_major_locator(MultipleLocator(20))
#axs[0,0].yaxis.set_minor_locator(MultipleLocator(10))
#axs[0,0].set_ylim([60,120])
axs[0].set_ylabel('Monthly Demand (acft)')


#axs[0,1].scatter(0, np.sum(Historic_use.iloc[80,2:14])-np.sum(Historic_use.iloc[80,2:14]), color = 'black')
axs[1].scatter(1, 100*(np.sum(Indoor_2100_ssp3_med.iloc[index,2:14] + Outdoor_2100_ssp3_med.iloc[index,2:14]) -  np.sum(Historic_use.iloc[hist_index,2:14]))/np.sum(Historic_use.iloc[hist_index,2:14]), color = 'green')
axs[1].scatter(2, 100*(np.sum(Indoor_2100_ssp5_lo.iloc[index,2:14] + Outdoor_2100_ssp5_lo.iloc[index,2:14]) - np.sum(Historic_use.iloc[hist_index,2:14]))/np.sum(Historic_use.iloc[hist_index,2:14]), color = 'blue')
axs[1].scatter(3, 100*(np.sum(Indoor_2100_ssp5_med.iloc[index,2:14] + Outdoor_2100_ssp5_med.iloc[index,2:14]) - np.sum(Historic_use.iloc[hist_index,2:14]))/np.sum(Historic_use.iloc[hist_index,2:14]), color = 'gold')
axs[1].scatter(4, 100*(np.sum(Indoor_2100_ssp5_hi.iloc[index,2:14] + Outdoor_2100_ssp5_hi.iloc[index,2:14]) - np.sum(Historic_use.iloc[hist_index,2:14]))/np.sum(Historic_use.iloc[hist_index,2:14]), color = 'orange')
axs[1].set_xticks([1,2,3,4], ['SSP3', 'SSP5, low', 'SSP5, med', 'SSP5, hi'], rotation = 90)
#axs[0,1].yaxis.set_major_locator(MultipleLocator(10))
#axs[0,1].yaxis.set_minor_locator(MultipleLocator(5))
#axs[0,1].set_ylim([-10,40])
axs[1].set_ylabel('% change')

plt.tight_layout()
