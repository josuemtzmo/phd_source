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
from trackeddy.physics import *
from trackeddy.plotfunc import *
from numpy import *
from scipy.interpolate import griddata

ensemble         =int(sys.argv[1])
year             =int(sys.argv[2])
file_division    =int(sys.argv[3])
division_number  =int(sys.argv[4])
file_count       =int(sys.argv[5])

def split_list(alist, wanted_parts=1):
    length = len(alist)
    return np.array([ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
             for i in range(wanted_parts) ])

outfile='/home/156/jm5970/data/trackeddy_output/OCCIPUT/npy/ORCA025.L75-OCCITENS.{0:03}/'.format(ensemble)

try:
    os.mkdir(outfile)
except:
    print('previous data overwritten')

# Output data path
outputpath='/g/data/x77/amh157/OCCIPUT/SSH_ENSEMBLE_all/ORCA025.L75-OCCITENS.%03d-S/' % ensemble

# Import SSH values to python environment.
ncfile=Dataset(outputpath+'1d/ORCA025.L75-OCCITENS.{0:03}_y{1}.1d_SSH.nc'.format(ensemble,year))
time=ncfile.variables['time_counter'][:]

time_division=split_list(range(0,len(time)), wanted_parts=file_division)
#print(time_division)

ssh=ncfile.variables['ssh'][time_division[division_number][0]:time_division[division_number][-1]+1,:,:]

# Import geographic coor#dinates (Lon,Lat)
lon=ncfile.variables['nav_lon'][:] 
lat=ncfile.variables['nav_lat'][:]

x=np.linspace(-180,180,shape(lon)[1])
y=np.linspace(-90,90,shape(lon)[0])
X,Y=meshgrid(x,y)

eta=np.zeros((shape(ssh)[0],len(y),len(x)))

for t in range(shape(ssh)[0]):
    eta[t,:,:]=griddata((lon.ravel(),lat.ravel()),ssh[t,:,:].ravel(),(X,Y),'linear')

eta=np.ma.masked_where(isnan(eta),eta)

# Import SSH 10 yrs mean values to python environment.
ncfile=Dataset('/g/data/v45/jm5970/trackeddy_output/OCCIPUT/pre-processing/ORCA025.L75-OCCITENS.{0:03}_y_mean.nc'.format(ensemble))
ssh_mean=squeeze(ncfile.variables['ssh'][:,:]).data

areamap=array([[0,len(x)],[0,len(y)]])

filters = {'time':{'type':'historical','t':None,'t0':None,'value':ssh_mean},
           'spatial':{'type':'moving','window':120,'mode':'uniform'}}

preferences={'ellipse':0.7,'eccentricity':0.95,'gaussian':0.7}

levels = {'max':nanmax(eta),'min':0.001,'step':0.001}
eddytd=analyseddyzt(eta,x,y,0,shape(eta)[0],1,levels,areamap=areamap,mask='',maskopt='forcefit',timeanalysis='none'\
                    ,preferences=preferences,filters=filters,destdir='',physics='',diagnostics=False,pprint=True)
print("Saving Positive",file_count)

save(outfile+'OCCIPUT_%05d_pos.npy' % file_count,eddytd)

levels = {'max':-nanmin(eta),'min':0.001,'step':0.001}
eddytdn=analyseddyzt(-eta,x,y,0,shape(eta)[0],1,levels,areamap=areamap,mask='',maskopt='forcefit',timeanalysis='none'\
                     ,preferences=preferences,filters=filters,destdir='',physics='',diagnostics=False,pprint=False)
print("Saving Negative")
save(outfile+'OCCIPUT_%05d_neg.npy' % file_count,eddytdn)
