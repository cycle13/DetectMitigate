"""
Plots timeseries of temperature over central Africa using SSP119 and
SSP245

Author     : Zachary M. Labe
Date       : 23 February 2023
Version    : 1 binary for ssp245 or ssp119
"""

### Import packages
import matplotlib.pyplot as plt
import numpy as np
import sys
from netCDF4 import Dataset
import palettable.cubehelix as cm
import palettable.cartocolors.qualitative as cc
import cmasher as cmr
import calc_dataFunctions as df
import calc_Utilities as UT
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid

### Plotting defaults 
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 

###############################################################################
###############################################################################
###############################################################################
### Plotting defaults 
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 

### Directories
directoryfigure = '/home/Zachary.Labe/Research/DetectMitigate/Figures/'
directoryoutput = '/home/Zachary.Labe/Research/DetectMitigate/Data/'

###############################################################################
###############################################################################
###############################################################################
### Data preliminaries 
modelGCMs = ['SPEAR_MED','SPEAR_MED_Scenario']
dataset_obs = 'ERA5_MEDS'
lenOfPicks = len(modelGCMs)
allDataLabels = modelGCMs
monthlychoice = 'annual'
variq = 'T2M'
reg_name = 'Globe'
level = 'surface'
###############################################################################
###############################################################################
randomalso = False
timeper = ['futureforcing','futureforcing']
scenarioall = ['SSP119','SSP245']
num_of_class = len(scenarioall)
shuffletype = 'GAUSS'
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
ensTypeExperi = 'ENS'
shuffletype = 'RANDGAUSS'
if window == 0:
    rm_standard_dev = False
    ravel_modelens = False
    ravelmodeltime = False
else:
    rm_standard_dev = True
    ravelmodeltime = False
    ravel_modelens = True
yearsall = [np.arange(2015+window,2100+1,1),
            np.arange(2015+window,2100+1,1)]

if variq == 'T2M':
    yearsobs = np.arange(1950+window,2021+1,1)
else:
    yearsobs = np.arange(1979+window,2021+1,1)
lentime = len(yearsall)
###############################################################################
###############################################################################
numOfEns = 30
numOfEns_10ye = 9
dataset_inference = True
###############################################################################
###############################################################################
lat_bounds,lon_bounds = UT.regions(reg_name)
###############################################################################
###############################################################################
ravelyearsbinary = False
ravelbinary = False
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

data_ssp119,lat1,lon1 = read_primary_dataset(variq,'SPEAR_MED_Scenario',monthlychoice,'SSP119',lat_bounds,lon_bounds)
data_ssp245,lat1,lon1 = read_primary_dataset(variq,'SPEAR_MED_Scenario',monthlychoice,'SSP245',lat_bounds,lon_bounds)

###############################################################################
###############################################################################
###############################################################################
### Calculate mean T2M over Central Africa
latmin = 0
latmax = 15
lonmin = 0
lonmax = 40
latq = np.where((lat1 >= latmin) & (lat1 <= latmax))[0]
lonq = np.where((lon1 >= lonmin) & (lon1 <= lonmax))[0]
latNA1 = lat1[latq]
lonNA1 = lon1[lonq]
lonNA2,latNA2 = np.meshgrid(lonNA1,latNA1)

NA_data_ssp1191 = data_ssp119[:,:,latq,:]
NA_data_ssp119 = NA_data_ssp1191[:,:,:,lonq]
ave_NA_data_ssp119 = UT.calc_weightedAve(NA_data_ssp119,latNA2)

data_ssp2451 = data_ssp245[:,:,latq,:]
NA_data_ssp245 = data_ssp2451[:,:,:,lonq]
ave_NA_data_ssp245 = UT.calc_weightedAve(NA_data_ssp245,latNA2)

### Calculate statistics for plot
max_ssp119 = np.nanmax(ave_NA_data_ssp119,axis=0)
min_ssp119 = np.nanmin(ave_NA_data_ssp119,axis=0)
mean_ssp119 = np.nanmean(ave_NA_data_ssp119,axis=0)

max_ssp245 = np.nanmax(ave_NA_data_ssp245,axis=0)
min_ssp245 = np.nanmin(ave_NA_data_ssp245,axis=0)
mean_ssp245 = np.nanmean(ave_NA_data_ssp245,axis=0)

minens = [min_ssp119,min_ssp245]
maxens = [max_ssp119,max_ssp245]
meanens = [mean_ssp119,mean_ssp245]
colors = ['teal','maroon']

###############################################################################
###############################################################################
###############################################################################               
### Plot Figure
### Adjust axes in time series plots 
def adjust_spines(ax, spines):
    for loc, spine in ax.spines.items():
        if loc in spines:
            spine.set_position(('outward', 5))
        else:
            spine.set_color('none')  
    if 'left' in spines:
        ax.yaxis.set_ticks_position('left')
    else:
        ax.yaxis.set_ticks([])

    if 'bottom' in spines:
        ax.xaxis.set_ticks_position('bottom')
    else:
        ax.xaxis.set_ticks([]) 
        
fig = plt.figure()
ax = plt.subplot(111)

adjust_spines(ax, ['left', 'bottom'])            
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.spines['bottom'].set_color('dimgrey')
ax.spines['left'].set_color('dimgrey')
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2)
ax.tick_params('both',length=4.,width=2,which='major',color='dimgrey')
ax.tick_params(axis='x',labelsize=6,pad=1.5)
ax.tick_params(axis='y',labelsize=6,pad=1.5)

for i in range(len(meanens)): 
    plt.fill_between(x=yearsall[i],y1=minens[i],y2=maxens[i],facecolor=colors[i],zorder=1,
              alpha=0.25,edgecolor='none',clip_on=False)
    plt.plot(yearsall[i],meanens[i],linestyle='-',linewidth=3.5,color=colors[i],
              label=r'\textbf{%s}' % scenarioall[i],zorder=1.5,clip_on=False,
              alpha=0.75)
    
plt.plot(yearsall[0],ave_NA_data_ssp119[-1],linestyle='--',linewidth=0.8,color='teal',
          clip_on=False,zorder=3,dashes=(1,0.3))
plt.plot(yearsall[1],ave_NA_data_ssp245[-1],linestyle='--',linewidth=0.8,color='maroon',
          clip_on=False,zorder=3,dashes=(1,0.3))

leg = plt.legend(shadow=False,fontsize=8,loc='upper center',
      bbox_to_anchor=(0.5,1.03),fancybox=True,ncol=3,frameon=False,
      handlelength=1,handletextpad=0.5)

plt.xticks(np.arange(1920,2101,10),np.arange(1920,2101,10))
plt.yticks(np.round(np.arange(-48,48.1,1),2),np.round(np.arange(-48,48.1,1),2))
plt.xlim([2015,2100])
plt.ylim([24,30])

plt.ylabel(r'\textbf{Central Africa T2M [$^{\circ}$C]}',
            fontsize=10,color='k')
plt.title(r'\textbf{CENTRAL AFRICA %s' % variq,fontsize=15,color='dimgrey')

plt.tight_layout()
plt.savefig(directoryfigure + 'CentralAfrica_%s_EmissionScenarios_%s_ssp119_245.png' % (variq,monthlychoice),dpi=300)
