"""
Plot land fractions to different SPEAR runs

Author    : Zachary M. Labe
Date      : 12 August 2023
"""

from netCDF4 import Dataset
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
import numpy as np
import cmocean
import cmasher as cmr
import calc_Utilities as UT
import calc_dataFunctions as df
import calc_Stats as dSS
import sys
import scipy.stats as sts
from scipy.interpolate import griddata as g

### Read in data files from server
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 

numOfEns = 30
numOfEns_10ye = 9
years = np.arange(2015,2100+1)

###############################################################################
###############################################################################
###############################################################################
### Data preliminaries 
directoryfigure = '/home/Zachary.Labe/Research/DetectMitigate/Figures/'
letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u"]
###############################################################################
###############################################################################
seasons = ['JJA']
slicemonthnamen = ['JJA']
monthlychoice = seasons[0]
reg_name = 'US'

epochsize = 10
simulations = ['SPEAR_MED','SPEAR_MED_SSP245','SPEAR_MED_LM42p2_test']
scenarios = ['SSP585','SPEAR_MED_SSP245','SPEAR_MED_LM42']

modelnames = ['SPEAR_MED_SSP585','SPEAR_MED_SSP245','SPEAR_MED_LM42_test']
variablenames = np.repeat(['frac_crop','frac_ntrl','frac_past','frac_scnd'],3)

###############################################################################
###############################################################################
###############################################################################
### Read in climate models      
def read_primary_dataset(variq,dataset,monthlychoice,scenario,lat_bounds,lon_bounds):
    data,lats,lons = df.readFiles(variq,dataset,monthlychoice,scenario)
    datar,lats,lons = df.getRegion(data,lats,lons,lat_bounds,lon_bounds)
    print('\nOur dataset: ',dataset,' is shaped',data.shape)
    return datar,lats,lons 

### Temporary regridding function
def regrid(lat11,lon11,lat21,lon21,var,years):
    """
    Interpolated on selected grid. Reads SPEAR in as 4d with 
    [year,lat,lon]
    """
    
    lon1,lat1 = np.meshgrid(lon11,lat11)
    lon2,lat2 = np.meshgrid(lon21,lat21)
    
    varn_re = np.reshape(var,((lat1.shape[0]*lon1.shape[1])))   
    
    print('Completed: Start regridding process:')
    varn = g((np.ravel(lat1),np.ravel(lon1)),varn_re,(lat2,lon2),method='linear')
    print('Completed: End Regridding---')
    return varn

def readData(simulation,scenario,epochsize):
    
    if simulation == 'SPEAR_MED_SSP245':
        
        data = Dataset('/work/Zachary.Labe/Data/SPEAR/SPEAR_MED_SSP245/monthly/frac_crop/frac_crop_01_2011-2100.nc')
        frac_crop = data.variables['frac_crop'][-86*12:].reshape(86,12,360,576)
        frac_cropm = np.nanmean(frac_crop[:,5:8,:,:],axis=1)
        lats = data.variables['lat'][:]
        lons = data.variables['lon'][:]
        data.close()
        
        data = Dataset('/work/Zachary.Labe/Data/SPEAR/SPEAR_MED_SSP245/monthly/frac_ntrl/frac_ntrl_01_2011-2100.nc')
        frac_ntrl = data.variables['frac_ntrl'][-86*12:].reshape(86,12,360,576)
        frac_ntrlm = np.nanmean(frac_ntrl[:,5:8,:,:],axis=1)
        data.close()
        
        data = Dataset('/work/Zachary.Labe/Data/SPEAR/SPEAR_MED_SSP245/monthly/frac_past/frac_past_01_2011-2100.nc')
        frac_past = data.variables['frac_past'][-86*12:].reshape(86,12,360,576)
        frac_pastm = np.nanmean(frac_past[:,5:8,:,:],axis=1)
        data.close()
        
        data = Dataset('/work/Zachary.Labe/Data/SPEAR/SPEAR_MED_SSP245/monthly/frac_scnd/frac_scnd_01_2011-2100.nc')
        frac_scnd = data.variables['frac_scnd'][-86*12:].reshape(86,12,360,576)
        frac_scndm = np.nanmean(frac_scnd[:,5:8,:,:],axis=1)
        data.close()
          
    else:      
        lat_bounds,lon_bounds = UT.regions('Globe')
        frac_crop,lats,lons = read_primary_dataset('frac_crop',simulation,monthlychoice,scenario,lat_bounds,lon_bounds)
        frac_ntrl,lats,lons = read_primary_dataset('frac_ntrl',simulation,monthlychoice,scenario,lat_bounds,lon_bounds)
        frac_past,lats,lons = read_primary_dataset('frac_past',simulation,monthlychoice,scenario,lat_bounds,lon_bounds)
        frac_scnd,lats,lons = read_primary_dataset('frac_scnd',simulation,monthlychoice,scenario,lat_bounds,lon_bounds)
        
        ### Calculate ensemble mean
        frac_cropm = np.nanmean(frac_crop,axis=0)
        frac_ntrlm = np.nanmean(frac_ntrl,axis=0)
        frac_pastm = np.nanmean(frac_past,axis=0)
        frac_scndm = np.nanmean(frac_scnd,axis=0)
        
    ### Slice for 2070
    years = np.arange(2015,2100+1,1)
    yearsactual = np.arange(2015,2070+1,1)
    yearq = np.where((years <= 2070))[0]
    if simulation != 'SPEAR_MED_LM42p2_test':
        frac_cropm = frac_cropm[yearq,:,:]
        frac_ntrlm = frac_ntrlm[yearq,:,:]
        frac_pastm = frac_pastm[yearq,:,:]
        frac_scndm = frac_scndm[yearq,:,:]
    
    diffcrop = np.nanmean(frac_cropm[-epochsize:,:,:] - frac_cropm[:epochsize,:,:],axis=0)
    diffntrl = np.nanmean(frac_ntrlm[-epochsize:,:,:] - frac_ntrlm[:epochsize,:,:],axis=0)
    diffpast = np.nanmean(frac_pastm[-epochsize:,:,:] - frac_pastm[:epochsize,:,:],axis=0) 
    diffscnd = np.nanmean(frac_scndm[-epochsize:,:,:] - frac_scndm[:epochsize,:,:],axis=0)
    
    if simulation == 'SPEAR_MED_LM42p2_test':
        data = Dataset('/work/Zachary.Labe/Data/SPEAR/SPEAR_MED_SSP245/monthly/frac_crop/frac_crop_01_2011-2100.nc')
        latss = data.variables['lat'][:]
        lonss = data.variables['lon'][:]
        data.close()
        
        diffcropr_raw = regrid(lats,lons,latss,lonss,diffcrop,yearsactual)
        diffntrlr_raw = regrid(lats,lons,latss,lonss,diffntrl,yearsactual)
        diffpastr_raw = regrid(lats,lons,latss,lonss,diffpast,yearsactual)
        diffscndr_raw = regrid(lats,lons,latss,lonss,diffscnd,yearsactual)
        
        ### Need to convert by area from units m2 to %
        data = Dataset('//work/Zachary.Labe/Data/SPEAR/SPEAR_MED_LM42p2_test/monthly/Metadata/atmos.static.nc')
        area = data.variables['area'][:]
        data.close()
        
        diffcropr = diffcropr_raw/area # m2/m2
        diffntrlr = diffntrlr_raw/area # m2/m2
        diffpastr = diffpastr_raw/area # m2/m2
        diffscndr = diffscndr_raw/area # m2/m2
        
        lats = latss
        lons = lonss
        
    else:
        diffcropr = diffcrop
        diffntrlr = diffntrl
        diffpastr = diffpast
        diffscndr = diffscnd

    return frac_cropm,frac_ntrlm,frac_pastm,frac_scndm,diffcropr,diffntrlr,diffpastr,diffscndr,lats,lons

frac_cropm_585,frac_ntrlm_585,frac_pastm_585,frac_scndm_585,diffcrop_585,diffntrl_585,diffpast_585,diffscnd_585,lats,lons = readData(simulations[0],scenarios[0],epochsize)
frac_cropm_245,frac_ntrlm_245,frac_pastm_245,frac_scndm_245,diffcrop_245,diffntrl_245,diffpast_245,diffscnd_245,lats,lons = readData(simulations[1],scenarios[1],epochsize)
frac_cropm_LM42,frac_ntrlm_LM42,frac_pastm_LM42,frac_scndm_LM42,diffcrop_LM42,diffntrl_LM42,diffpast_LM42,diffscnd_LM42,lats,lons = readData(simulations[2],scenarios[2],epochsize)

preparedata = [diffcrop_585,diffcrop_245,diffcrop_LM42,
                diffntrl_585,diffntrl_245,diffntrl_LM42,
                diffpast_585,diffpast_245,diffpast_LM42,
                diffscnd_585,diffscnd_245,diffscnd_LM42]

###############################################################################
###############################################################################
###############################################################################
### Plot differences in land fraction
fig = plt.figure(figsize=(9,6))

label = r'\textbf{Fraction = 2091-2100 minus 2015-2024}'
limit = np.arange(-0.3,0.31,0.01)
barlim = np.round(np.arange(-0.3,0.4,0.1),2)
cmap = cmocean.cm.balance

for i in range(len(preparedata)):
    ax = plt.subplot(4,3,i+1)
    
    var = preparedata[i]
    lat1 = lats
    lon1 = lons
    
    m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
                projection='lcc',lat_1=33,lat_2=45,lon_0=-95,resolution='l',
                area_thresh=10000)
    m.drawcoastlines(color='darkgrey',linewidth=1)
    m.drawstates(color='darkgrey',linewidth=0.5)
    m.drawcountries(color='darkgrey',linewidth=0.5)

    circle = m.drawmapboundary(fill_color='dimgrey',color='dimgrey',
                      linewidth=0.7)
    circle.set_clip_on(False)
        
    lon2,lat2 = np.meshgrid(lon1,lat1)
    
    cs1 = m.contourf(lon2,lat2,var,limit,extend='both',latlon=True)
    
    cs1.set_cmap(cmap)
    
    ax.annotate(r'\textbf{[%s]}' % (letters[i]),xy=(0,0),xytext=(0.0,1.06),
              textcoords='axes fraction',color='k',fontsize=7,
              rotation=0,ha='center',va='center')
    
    if any([i==0,i==3,i==6,i==9]):
        ax.annotate(r'\textbf{%s}' % (variablenames[i]),xy=(0,0),xytext=(-0.1,0.5),
                  textcoords='axes fraction',color='dimgrey',fontsize=11,
                  rotation=90,ha='center',va='center')     
    if any([i==0,i==1,i==2]):
        ax.annotate(r'\textbf{%s}' % (modelnames[i]),xy=(0,0),xytext=(0.5,1.2),
                  textcoords='axes fraction',color='k',fontsize=7,
                  rotation=0,ha='center',va='center')       
    
cbar_ax1 = fig.add_axes([0.29,0.06,0.4,0.02])                
cbar1 = fig.colorbar(cs1,cax=cbar_ax1,orientation='horizontal',
                    extend='both',extendfrac=0.07,drawedges=False)
cbar1.set_label(label,fontsize=8,color='k',labelpad=5)  
cbar1.set_ticks(barlim)
cbar1.set_ticklabels(list(map(str,barlim)))
cbar1.ax.tick_params(axis='x', size=.01,labelsize=7)
cbar1.outline.set_edgecolor('dimgrey')

plt.tight_layout()
plt.subplots_adjust(bottom=0.13,top=0.93,hspace=0.15,wspace=-0.4)
        
plt.savefig(directoryfigure + 'FutureLandChange_SSPs-LM42_JJA.png',dpi=300)
