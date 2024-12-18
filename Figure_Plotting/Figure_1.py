# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import os 
import matplotlib.pyplot as plt

os.chdir() # Path to Step 4 Folder 

historic_demand = pd.read_csv("Historical_use_master.csv", index_col = 0)

for i in range(85):
    if historic_demand.iloc[i,0] == 'CTY_SFE':
        plt.plot(historic_demand.iloc[i,1:]/min(historic_demand.iloc[i,1:]), color = 'red')
    else:
        plt.plot(historic_demand.iloc[i,1:]/min(historic_demand.iloc[i,1:]), color = 'grey', alpha = 0.1)
plt.ylabel("Reletive monthly use [-]")

for i in range(85):
    if historic_demand.iloc[i,0] == 'CTY_SFE':
        plt.plot(historic_demand.iloc[i,1:], color = 'red')
    else:
        plt.plot(historic_demand.iloc[i,1:], color = 'grey', alpha = 0.2)
        
plt.ylim([0,4000])
