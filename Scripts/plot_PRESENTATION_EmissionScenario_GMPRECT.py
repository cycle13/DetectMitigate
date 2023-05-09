"""
Plot GMPRECT for the different SPEAR emission scenarios

Author     : Zachary M. Labe
Date       : 5 January 2022
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
import read_ERA5_monthlyMEDS as E
import scipy.stats as sts

### Plotting defaults 
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 
plt.rc('savefig',facecolor='black')
plt.rc('axes',edgecolor='darkgrey')
plt.rc('xtick',color='darkgrey')
plt.rc('ytick',color='darkgrey')
plt.rc('axes',labelcolor='darkgrey')
plt.rc('axes',facecolor='black')

### Directories
directoryfigure = '/home/Zachary.Labe/Research/DetectMitigate/Dark_Figures/'
directoryoutput = '/home/Zachary.Labe/Research/DetectMitigate/Data/'

###############################################################################
###############################################################################
###############################################################################
### Data preliminaries 
modelGCMs = ['SPEAR_MED_Historical','SPEAR_MED_NATURAL','SPEAR_MED',
             'SPEAR_MED_Scenario','SPEAR_MED_Scenario','SPEAR_MED_Scenario',
             'SPEAR_MED_SSP534OS_10ye']
dataset_obs = 'ERA5_MEDS'
lenOfPicks = len(modelGCMs)
monthlychoice = 'annual'
variq = 'PRECT'
reg_name = 'Globe'
level = 'surface'
###############################################################################
###############################################################################
timeper = ['historicalforcing','futureforcing','futureforcing','futureforcing','futureforcing','futureforcing','futureforcing']
scenarioall = ['historical','natural','SSP585','SSP119','SSP245','SSP534OS','SSP534OS_10ye']
###############################################################################
###############################################################################
land_only = False
ocean_only = False
###############################################################################
###############################################################################
baseline = np.arange(1981,2010+1,1)
###############################################################################
###############################################################################
window = 0
yearsall = [np.arange(1929+window,2014+1,1),np.arange(2015+window,2100+1,1),
            np.arange(2015+window,2100+1,1),np.arange(2015+window,2100+1,1),
            np.arange(2015+window,2100+1,1),np.arange(2015+window,2100+1,1),
            np.arange(2015+window,2100+1,1)]
yearsobs = np.arange(1979+window,2021+1,1)
###############################################################################
###############################################################################
numOfEns = 30
numOfEns_10ye = 9
lentime = len(yearsall)
###############################################################################
###############################################################################
# lat_bounds,lon_bounds = UT.regions(reg_name)
# ###############################################################################
# ###############################################################################
# ###############################################################################
# ###############################################################################
# ### Read in model and observational/reanalysis data
# def read_primary_dataset(variq,dataset,monthlychoice,scenario,lat_bounds,lon_bounds):
#     data,lats,lons = df.readFiles(variq,dataset,monthlychoice,scenario)
#     datar,lats,lons = df.getRegion(data,lats,lons,lat_bounds,lon_bounds)
#     print('\nOur dataset: ',dataset,' is shaped',data.shape)
#     return datar,lats,lons 

# ### Loop in all climate models
# data_all = []
# for no in range(len(modelGCMs)):
#     dataset = modelGCMs[no]
#     scenario = scenarioall[no]
#     data_allq,lats,lons = read_primary_dataset(variq,dataset,monthlychoice,scenario,lat_bounds,lon_bounds)
#     data_all.append(data_allq)
# data = data_all

# ### Calculate historical baseline for calculating anomalies (and ensemble mean)
# historical = data[0]
# historicalyrs = yearsall[0]

# yearhq = np.where((historicalyrs >= baseline.min()) & (historicalyrs <= baseline.max()))[0]
# historicalc = np.nanmean(np.nanmean(historical[:,yearhq,:,:],axis=1),axis=0)

# ### Calculate anomalies
# data_anom = []
# for no in range(len(modelGCMs)):
#     anomq = data[no] - historicalc[np.newaxis,np.newaxis,:,:]
#     data_anom.append(anomq)

# ### Calculate global average
# lon2,lat2 = np.meshgrid(lons,lats)
# aveall = []
# maxens = []
# minens = []
# meanens = []
# medianens = []
# for no in range(len(modelGCMs)):
#     aveallq = UT.calc_weightedAve(data_anom[no],lat2)

#     maxensq = np.nanmax(aveallq,axis=0)
#     minensq = np.nanmin(aveallq,axis=0)
#     meanensq = np.nanmean(aveallq,axis=0)
#     medianensq = np.nanmedian(aveallq,axis=0)
    
#     aveall.append(aveallq)
#     maxens.append(maxensq)
#     minens.append(minensq)
#     meanens.append(meanensq)
#     medianens.append(medianensq)

# ### Read in observations from ERA5 and regrid onto SPEAR
# latobs1,lonobs1,levobs,varobs = E.read_ERA5_monthlyMEDS(variq,'/work/Zachary.Labe/Data/',
#                                                   monthlychoice,yearsobs,3,True,np.nan,
#                                                   'surface')
# lonobs2,latobs2 = np.meshgrid(lonobs1,latobs1)

# yearhqo = np.where((yearsobs >= baseline.min()) & (yearsobs <= baseline.max()))[0]
# climobs = np.nanmean(varobs[yearhqo,:,:],axis=0)
# anomobs = varobs - climobs
# aveobs = UT.calc_weightedAve(anomobs,latobs2)

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
ax.spines['bottom'].set_color('darkgrey')
ax.spines['left'].set_color('darkgrey')
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2)
ax.tick_params('both',length=4.,width=2,which='major',color='darkgrey')
ax.tick_params(axis='x',labelsize=6,pad=1.5)
ax.tick_params(axis='y',labelsize=6,pad=1.5)

color = cmr.rainforest(np.linspace(0.2,0.93,len(aveall)))
for i,c in zip(range(len(aveall)),color): 
    if i == 0:
        c = 'w'
    plt.fill_between(x=yearsall[i],y1=minens[i],y2=maxens[i],facecolor=c,zorder=1,
             alpha=0.4,edgecolor='none',clip_on=False)
    plt.plot(yearsall[i],meanens[i],linestyle='-',linewidth=2,color=c,
             label=r'\textbf{%s}' % scenarioall[i],zorder=2,clip_on=False)

# plt.plot(yearsobs,aveobs,linestyle='--',linewidth=0.8,color='r',
#          dashes=(1,0.5),clip_on=False,zorder=30,label=r'\textbf{ERA5}')

leg = plt.legend(shadow=False,fontsize=8,loc='upper center',
      bbox_to_anchor=(0.5,1.05),fancybox=True,ncol=3,frameon=False,
      handlelength=1,handletextpad=0.5)
for line,text in zip(leg.get_lines(), leg.get_texts()):
    text.set_color(line.get_color())

plt.xticks(np.arange(1920,2101,10),np.arange(1920,2101,10))
plt.yticks(np.round(np.arange(-0.5,0.51,0.1),2),np.round(np.arange(-0.5,0.51,0.1),2))
plt.xlim([1930,2100])
plt.ylim([-0.1,0.3])

plt.ylabel(r'\textbf{Precipitation Anomaly [mm/day] Relative to 1951-1980}',
           fontsize=7,color='darkgrey')

plt.tight_layout()
plt.savefig(directoryfigure + 'PRESENTATION_GMPRECT_EmissionScenarios_%s.png' % monthlychoice,dpi=300)
