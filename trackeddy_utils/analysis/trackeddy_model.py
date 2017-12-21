import matplotlib
matplotlib.use('agg')
import sys
from netCDF4 import Dataset
import os
import cmocean as cm
from trackeddy.tracking import *
from trackeddy.datastruct import *
from trackeddy.geometryfunc import *
from trackeddy.init import *
from trackeddy.physics import *
from trackeddy.plotfunc import *
from numpy import *


outputfilenumber=sys.argv[1]
outfile='/g/data/v45/jm5970/trackeddy_out/'

# Output data path
outputpath='/g/data/v45/akm157/model_output/mom/mom01v5_kds75/output'+outputfilenumber+'/'
# Import SSH values to python environment.
ncfile=Dataset(outputpath+'rregionsouthern_ocean_daily_eta_t.nc')
eta=ncfile.variables['eta_t'][:]*100
# Import geographic coordinates (Lon,Lat)
lon=ncfile.variables['xt_ocean_sub01'][:]
lat=ncfile.variables['yt_ocean_sub01'][:]

# Import SSH 10 yrs mean values to python environment.
ncfile=Dataset('/g/data/v45/jm5970/data.input/meanssh_10yrs_AEXP.nc')
ssh_mean=squeeze(ncfile.variables['SSH_mean'][:])
# Import geographic coordinates (Lon,Lat)
lon=ncfile.variables['Longitude'][:]
lat=ncfile.variables['Latitude'][:]

areamap=array([[0,len(lon)],[0,len(lat)]])

eddytd=analyseddyzt(eta,lon,lat,0,shape(eta)[0],1,25,5,5,data_meant=ssh_mean,areamap=areamap,mask=''\
                     ,destdir='',physics='',diagnostics=False,pprint=False)
save(outfile+outputfilenumber+'_pos.npy',eddytd)

eddytd=''

eddytdn=analyseddyzt(eta,lon,lat,0,shape(eta)[0],1,-25,-5,-5,data_meant=ssh_mean,areamap='',mask=''\
                     ,destdir='',physics='',diagnostics=False,pprint=False)
save(outfile+outputfilenumber+'_neg.npy',eddytdn)

eddytdn=''
