import matplotlib
matplotlib.use('agg')
from calendar import monthrange
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

year=sys.argv[1]
monthsin=int(sys.argv[2])
monthsend=int(sys.argv[3])

print('Analizing the year ',year,'in the months[',monthsin,'-',monthsend,']')
inputfiles='/g/data/ua8/CMEMS_SeaLevel/v4-0/'+year+'/'
#inputfiles='/g/data/ua8/CMEMS_SeaLevel/v3-0/'+year+'/'

outfile='/g/data/v45/jm5970/trackeddy_out/'

ii=0

datashapetime=0
for month in range(monthsin,monthsend):
    datashapetime=datashapetime+monthrange(int(year), month)[1]
try:
    ncfile=Dataset(inputfiles+'dt_global_allsat_phy_l4_'+year+'0101_20180115.nc')
except:
    ncfile=Dataset(inputfiles+'dt_global_allsat_phy_l4_'+year+'0101_20180516.nc')

#ncfile=Dataset(inputfiles+'dt_global_allsat_phy_l4_'+year+'0101_20170110.nc')
ssha=squeeze(ncfile.variables['sla'][:])
lon=ncfile.variables['longitude'][:]
lat=ncfile.variables['latitude'][:]

sshatime=zeros([datashapetime,shape(ssha)[0],shape(ssha)[1]])
ii=0
print('Start loading data')
for month in range(monthsin,monthsend):
    daysmonth=monthrange(int(year), month)[1]
    for days in range(1,daysmonth+1):
        try:
            ncfile=Dataset(inputfiles+'dt_global_allsat_phy_l4_'+year+'%02d'%month+'%02d'%days+'_20180115.nc')
        except:
            ncfile=Dataset(inputfiles+'dt_global_allsat_phy_l4_'+year+'%02d'%month+'%02d'%days+'_20180516.nc')
        #ncfile=Dataset(inputfiles+'dt_global_allsat_phy_l4_'+year+'%02d'%month+'%02d'%days+'_20170110.nc')
        sshatime[ii,:,:]=squeeze(ncfile.variables['sla'][:])
        ii=ii+1
        ncfile.close()

sshatime=ma.masked_where(sshatime <= -2147483647, sshatime)
print('End loading data')

areamap=array([[0,len(lon)],[0,len(lat)]])
#areamap=array([[0,len(lon)],[0,int(len(lat)/3)]])


filters = {'time':{'type':None,'t':None,'t0':None,'value':None},
           'spatial':{'type':'moving','window':50,'mode':'uniform'}}
levels = {'max':sshatime.max(),'min':0.01,'step':0.01}

eddytd=analyseddyzt(sshatime,lon,lat,0,shape(sshatime)[0],1,levels,areamap=areamap,mask=''\
                     ,filters=filters,destdir='',physics='',diagnostics=False,pprint=False)
print("Saving Positive")
save(outfile+year+str(monthsin)+'-'+str(monthsend)+'_pos_satellite.npy',eddytd)

levels = {'max':sshatime.min(),'min':-0.01,'step':-0.01}

eddytdn=analyseddyzt(sshatime,lon,lat,0,shape(sshatime)[0],1,levels,areamap=areamap,mask=''\
                     ,filters=filters,destdir='',physics='',diagnostics=False,pprint=True)
print("Saving Negative")
save(outfile+year+str(monthsin)+'-'+str(monthsend)+'_neg_satellite.npy',eddytdn)
