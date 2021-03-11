import matplotlib
matplotlib.use('agg')
import sys
from netCDF4 import Dataset
import xarray as xr
import os
os.environ["PROJ_LIB"] = "/g/data/v45/jm5970/env/track_env/share/proj"
import cmocean as cm
from trackeddy.tracking import *
from trackeddy.datastruct import *
from trackeddy.geometryfunc import *
from trackeddy.physics import *
from numpy import *

outputfilenumber = int(sys.argv[1])
division_number  = int(sys.argv[2])
file_division    = int(sys.argv[3])
file_count       = int(sys.argv[4]) 
outfile          = sys.argv[5]

def split_list(alist, wanted_parts=1):
    length = len(alist)
    return np.array([ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
             for i in range(wanted_parts) ])

#outfile='/g/data/v45/jm5970/trackeddy_output/ACCESS_OM2-01/npy/'

# Output data path
# outputpath='/g/data3/hh5/tmp/cosima/access-om2-025/025deg_jra55v13_iaf_gmredi6/output%03d/' % outputfilenumber
outputpath='/g/data/cj50/access-om2/raw-output/access-om2-01/01deg_jra55v140_iaf/output%03d/' % outputfilenumber

# Import SSH values to python environment.
ncfile=xr.open_mfdataset(outputpath+'ocean/ocean-2d-sea_level-1-daily-mean-ym_*.nc',combine='by_coords')
time=ncfile.time.values[:]

time_division=split_list(range(0,len(time)), wanted_parts=file_division)
#print(time_division)

eta=ncfile.sea_level.values[time_division[division_number][0]:time_division[division_number][-1]+1,:,:]
#print(np.shape(eta))

# Import geographic coor#dinates (Lon,Lat)
lon=ncfile.xt_ocean.values[:] 
lat=ncfile.yt_ocean.values[:]

# Import SSH 10 yrs mean values to python environment.
ncfile=Dataset('/g/data/v45/jm5970/trackeddy_output/ACCESS_OM2-01/pre-processing/ACCESS-OM2_01d_eta_mean.nc')
ssh_mean=squeeze(ncfile.variables['sea_level'][:,:]).data

areamap=array([[0,len(lon)],[0,len(lat)]])

filters = {'time':{'type':'historical','t':None,'t0':None,'value':ssh_mean},
           'spatial':{'type':'moving','window':120,'mode':'uniform'}}

preferences={'ellipse':0.7,'eccentricity':0.95,'gaussian':0.7}

print("Analysing",outputfilenumber, division_number)
step = 0.002

#levels = {'max':np.nanmax(eta),'min':step,'step':step}
#eddytd=analyseddyzt(eta,lon,lat,0,shape(eta)[0],1,levels,areamap=areamap,mask='',maskopt='forcefit',timeanalysis='none'\
#                    ,preferences=preferences,filters=filters,destdir='',physics='',diagnostics=False,pprint=False)
#print("Saving Positive",outputfilenumber, division_number) 

#save(outfile+'/ACCESS_01_{0:05}_{1:02}_pos.npy'.format(outputfilenumber,division_number),eddytd)

levels = {'max':-np.nanmin(eta),'min':step,'step':step}
eddytdn=analyseddyzt(-eta,lon,lat,0,shape(eta)[0],1,levels,areamap=areamap,mask='',maskopt='forcefit',timeanalysis='none'\
                     ,preferences=preferences,filters=filters,destdir='',physics='',diagnostics=False,pprint=False)
print("Saving Negative",outputfilenumber, division_number)
save(outfile+'/ACCESS_01_{0:05}_{1:02}_neg.npy'.format(outputfilenumber,division_number),eddytdn)
