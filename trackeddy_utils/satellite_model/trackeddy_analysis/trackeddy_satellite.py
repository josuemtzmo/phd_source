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
from trackeddy.physics import *
from trackeddy.plotfunc import *
from numpy import *

#monthsend=int(sys.argv[3])
from os import listdir
from os.path import isfile, join

year=sys.argv[1]
index_files=int(sys.argv[2])
divisions=int(sys.argv[3])

inputfiles='/g/data/ua8/CMEMS_SeaLevel/v4-0/'+year+'/'

onlyfiles = [join(inputfiles, f) for f in listdir(inputfiles) if isfile(join(inputfiles, f))]

onlyfiles.sort()

print(onlyfiles)

def split_list(alist, wanted_parts=1):
    length = len(alist)
    return np.array([ alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
             for i in range(wanted_parts) ])

files2analyse=split_list(onlyfiles, divisions)

print('Analizing the year ',year,'from file ',files2analyse[index_files][0],'-',files2analyse[index_files][-1],']')
#inputfiles='/g/data/ua8/CMEMS_SeaLevel/v3-0/'+year+'/'

outfile='/g/data/v45/jm5970/trackeddy_output/AVISO+/npy/'

datashapetime=len(files2analyse[index_files])

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

for files in files2analyse[index_files]:
    ncfile=Dataset(files)
    sshatime[ii,:,:]=squeeze(ncfile.variables['sla'][:])
    ii=ii+1
    ncfile.close()

#for month in range(monthsin,monthsend):
#    daysmonth=monthrange(int(year), month)[1]
#    for days in range(1,daysmonth+1):
#        print(inputfiles+'dt_global_allsat_phy_l4_'+year+'%02d'%month+'%02d'%days+'_20180115.nc')
#        try:
#            ncfile=Dataset(inputfiles+'dt_global_allsat_phy_l4_'+year+'%02d'%month+'%02d'%days+'_20180115.nc')
#        except:
#            ncfile=Dataset(inputfiles+'dt_global_allsat_phy_l4_'+year+'%02d'%month+'%02d'%days+'_20180516.nc')
#        
#        sshatime[ii,:,:]=squeeze(ncfile.variables['sla'][:])
#        ii=ii+1
#        ncfile.close()

sshatime=ma.masked_where(sshatime <= -2147483647, sshatime)
print('End loading data')

areamap=array([[0,len(lon)],[0,len(lat)]])

filters = {'time':{'type':None,'t':None,'t0':None,'value':None},
           'spatial':{'type':'moving','window':51,'mode':'uniform'}}
levels = {'max':sshatime.max(),'min':0.001,'step':0.001}

eddytd=analyseddyzt(sshatime,lon,lat,0,shape(sshatime)[0],1,levels,areamap=areamap,mask='',timeanalysis='none'\
                     ,filters=filters,destdir='',physics='',diagnostics=False,pprint=False)
print("Saving Positive")
save("{0}aviso_{1}-{2:03}_pos.npy".format(outfile,year,index_files),eddytd)

#levels = {'max':-sshatime.min(),'min':0.001,'step':0.001}

#eddytdn=analyseddyzt(-sshatime,lon,lat,0,shape(sshatime)[0],1,levels,areamap=areamap,mask='',timeanalysis='none'\
#                     ,filters=filters,destdir='',physics='',diagnostics=False,pprint=True)
#print("Saving Negative")
#save("{0}aviso_{1}-{2:03}_neg.npy".format(outfile,year,index_files),eddytdn)
