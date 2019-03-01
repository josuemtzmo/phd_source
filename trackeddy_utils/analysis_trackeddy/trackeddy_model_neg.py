import matplotlib
matplotlib.use('agg')
import sys
from netCDF4 import Dataset
import os
os.environ["PROJ_LIB"] = "/g/data/v45/jm5970/env/track_env/share/proj"
import cmocean as cm
from trackeddy.tracking import *
from trackeddy.datastruct import *
from trackeddy.geometryfunc import *
from trackeddy.init import *
from trackeddy.physics import *
from trackeddy.plotfunc import *
from numpy import *

outputfilenumber =int(sys.argv[1])
division_number  =int(sys.argv[2])
file_division    =int(sys.argv[3])
file_count       =int(sys.argv[4]) 

def split_list(alist, wanted_parts=1):
    length = len(alist)
    return np.array([ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
             for i in range(wanted_parts) ])

outfile='/g/data/v45/jm5970/trackeddy_out/model/'

# Output data path
outputpath='/g/data3/hh5/tmp/cosima/access-om2-01/01deg_jra55v13_iaf/output%03d/' % outputfilenumber

# Import SSH values to python environment.
ncfile=Dataset(outputpath+'ocean/ocean_daily.nc')
time=ncfile.variables['time'][:]

time_division=split_list(range(0,len(time)), wanted_parts=file_division)
#print(time_division)

eta=ncfile.variables['eta_t'][time_division[division_number][0]:time_division[division_number][-1],:,:]
#print(np.shape(eta))

# Import geographic coor#dinates (Lon,Lat)
lon=ncfile.variables['xt_ocean'][:] 
lat=ncfile.variables['yt_ocean'][:]

# Import SSH 10 yrs mean values to python environment.
ncfile=Dataset('/home/156/jm5970/data/github/trackeddy/data.input/ACCESS-OM2_01d_eta_mean.nc')
ssh_mean=squeeze(ncfile.variables['eta_t'][:])

# Import geographic coordinates (Lon,Lat)
#lon=ncfile.variables['Longitude'][:]
#lat=ncfile.variables['Latitude'][:]

areamap=array([[0,len(lon)],[0,len(lat)]])

filters = {'time':{'type':'historical','t':None,'t0':None,'value':ssh_mean},
           'spatial':{'type':'moving','window':120,'mode':'uniform'}}

preferences={'ellipse':0.70,'eccentricity':0.95,'gaussian':0.7}

#levels = {'max':eta.max(),'min':0.01,'step':0.01}
#eddytd=analyseddyzt(eta,lon,lat,0,shape(eta)[0],1,levels,areamap=areamap,mask='',maskopt='forcefit'\
#                    ,preferences=preferences,filters=filters,destdir='',physics='',diagnostics=False,pprint=True)
#print("Saving Positive",file_count)
#save(outfile+'%05d_pos.npy' % file_count,eddytd)

levels = {'max':-eta.min(),'min':0.01,'step':0.01}
eddytdn=analyseddyzt(-eta,lon,lat,0,shape(eta)[0],1,levels,areamap=areamap,mask='',maskopt='forcefit'\
                     ,preferences=preferences,filters=filters,destdir='',physics='',diagnostics=False,pprint=False)
print("Saving Negative",file_count)
save(outfile+'%05d_neg.npy' % file_count,eddytdn)
