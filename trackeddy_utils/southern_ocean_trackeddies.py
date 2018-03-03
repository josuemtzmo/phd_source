# Importing all libraries.
from pylab import *
from netCDF4 import Dataset
%matplotlib inline
import os
import cmocean as cm
from trackeddy.tracking import *
from trackeddy.datastruct import *
from trackeddy.geometryfunc import *
from trackeddy.init import *
from trackeddy.physics import *
from trackeddy.plotfunc import *

#import cosima_cookbook as cc

# Output data path

# Import SSH 10 yrs mean values to python environment.
ncfile=Dataset('/home/156/jm5970/notebooks/traceddy/data.output/meanssh_10yrs_AEXP.nc')
infile='/g/data/v45/akm157/model_output/mom/mom01v5_kds75/'
outfile='/g/data/v45/jm5970/trackeddy_out/'
ssh_mean=squeeze(ncfile.variables['SSH_mean'][:])
# Import geographic coordinates (Lon,Lat)
lon=ncfile.variables['Longitude'][:]
lat=ncfile.variables['Latitude'][:]

it=306
et=345

for tt in range(it,et):
    ncfile=Dataset(infile+'output'+str(tt)+'/rregionsouthern_ocean_daily_eta_t.nc')
    eta=ncfile.variables['eta_t'][:]*100
    mask=ma.getmask(eta[0,:,:])
    ssha=eta-ssh_mean
    eddytd=analyseddyzt(eta,lon,lat,0,shape(eta)[0],1,25,5,1,data_meant=ssh_mean,areamap=areamap,mask=''\
                        ,destdir='',okparm='',diagnostics=False,pprint=False)
    eddytdn=analyseddyzt(eta,lon,lat,0,shape(eta)[0],1,-25,-5,-1,data_meant=ssh_mean,areamap=areamap,\
                         mask='',destdir='',okparm='',diagnostics=False,pprint=False)
    
    save(outfile+str(tt)+'_pos.txt',eddytd)
    save(outfile+str(tt)+'_neg.txt',eddytd)