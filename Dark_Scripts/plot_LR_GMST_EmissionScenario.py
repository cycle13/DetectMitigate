"""
Plot GMST for the different SPEAR emission scenarios

Author     : Zachary M. Labe
Date       : 13 July 2023
Version    : 1 
"""

### Import packages
import sys
import matplotlib.pyplot as plt
import cmocean
import cmasher as cmr
import numpy as np
import calc_Utilities as UT
import calc_dataFunctions as df
import calc_Stats as dSS
import read_BEST as B
from scipy.interpolate import griddata as g
import scipy.stats as sts

### Plotting defaults 
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']})

### Directories
directoryfigure = '/home/Zachary.Labe/Research/DetectMitigate/Figures/'

###############################################################################
###############################################################################
###############################################################################
### Data preliminaries 
modelGCMs = ['SPEAR_MED_Historical','SPEAR_MED_NATURAL','SPEAR_MED',
             'SPEAR_MED_Scenario','SPEAR_MED_Scenario']
dataset_obs = 'ERA5_MEDS'
lenOfPicks = len(modelGCMs)
monthlychoice = 'annual'
variq = 'T2M'
reg_name = 'Globe'
level = 'surface'
###############################################################################
###############################################################################
timeper = ['historicalforcing','futureforcing','futureforcing','futureforcing','futureforcing']
scenarioall = ['historical','natural','SSP585','SSP119','SSP245']
###############################################################################
###############################################################################
land_only = False
ocean_only = False
###############################################################################
###############################################################################
baseline = np.arange(1951,1980+1,1)
###############################################################################
###############################################################################
window = 0
yearsall = [np.arange(1929+window,2014+1,1),np.arange(2015+window,2100+1,1),
            np.arange(2015+window,2100+1,1),np.arange(2015+window,2100+1,1),
            np.arange(2015+window,2100+1,1)]
yearsobs = np.arange(1929+window,2021+1,1)
###############################################################################
###############################################################################
numOfEns = 30
lentime = len(yearsall)
###############################################################################
###############################################################################
lat_bounds,lon_bounds = UT.regions(reg_name)
###############################################################################
###############################################################################
###############################################################################
###############################################################################
### Read in model and observational/reanalysis data
def read_primary_dataset(variq,dataset,monthlychoice,scenario,lat_bounds,lon_bounds):
    data,lats,lons = df.readFiles(variq,dataset,monthlychoice,scenario)
    datar,lats,lons = df.getRegion(data,lats,lons,lat_bounds,lon_bounds)
    print('\nOur dataset: ',dataset,' is shaped',data.shape)
    return datar,lats,lons 

### Loop in all climate models
data_all = []
for no in range(len(modelGCMs)):
    dataset = modelGCMs[no]
    scenario = scenarioall[no]
    data_allq,lats,lons = read_primary_dataset(variq,dataset,monthlychoice,scenario,lat_bounds,lon_bounds)
    data_all.append(data_allq)
data = np.asarray(data_all)

### Calculate global average
lon2,lat2 = np.meshgrid(lons,lats)

## Calculate global mean
gmt2m= UT.calc_weightedAve(data,lat2)

### Save time series
directoryoutput = '/home/Zachary.Labe/Research/DetectMitigate/Data/TimeSeries/'
np.save(directoryoutput + 'GMT2M_EmissionScenario.npy',gmt2m)
