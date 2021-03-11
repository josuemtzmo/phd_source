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

outputfilenumber =int(sys.argv[1])
init=50
end=77

expt='layer2_tau3e-1_manyshortridgesCorrectTopo'

layer=1

outfile='/g/data/v45/jm5970/trackeddy_output/simple_ocean_w_ridges/{0}/npy/'.format(expt)

# Output data path
outputpath='/g/data/v45/nc3020/EddySaturationBcBtSimulations_GRL2019/layer2/{0}/output{1:03}/'.format(expt,outputfilenumber)

# Import SSH values to python environment.
ncfile=Dataset(outputpath+'prog.nc')
time=ncfile.variables['Time'][:]

eta = squeeze(ncfile.variables['e'][:,layer,:,:])
#print(np.shape(eta))

# Import geographic coor#dinates (Lon,Lat)
lon=ncfile.variables['xh'][:] 
lat=ncfile.variables['yh'][:]

# Import SSH 10 yrs mean values to python environment.
ncfile=Dataset('/g/data/v45/jm5970/trackeddy_output/simple_ocean_w_ridges/{0}/pre-processing/mean_ssh_{1:03}_{2:03}.nc'.format(expt,init,end))
ssh_mean=squeeze(ncfile.variables['e'][layer,:,:])

# Import geographic coordinates (Lon,Lat)
#lon=ncfile.variables['Longitude'][:]
#lat=ncfile.variables['Latitude'][:]

areamap=array([[0,len(lon)],[0,len(lat)]])

filters = {'time':{'type':'historical','t':None,'t0':None,'value':ssh_mean},
           'spatial':{'type':None,'window':None,'mode':None}}

preferences={'ellipse':0.85,'eccentricity':0.95,'gaussian':0.85}
areaparm={'constant':np.inf}

levels = {'max':(eta-ssh_mean).max(),'min':0.001,'step':0.001}
eddytd=analyseddyzt(eta,lon,lat,0,shape(eta)[0],1,levels,areamap=areamap,mask='',maskopt='forcefit',timeanalysis='none'\
                    ,preferences=preferences,filters=filters,areaparms=areaparm,destdir='',physics='',diagnostics=False,pprint=True)
print("Saving Positive",outputfilenumber)
save(outfile+'2layer_{0:05}_{1}_pos.npy'.format(outputfilenumber,layer),eddytd)

levels = {'max':-(eta-ssh_mean).min(),'min':0.001,'step':0.001}
eddytdn=analyseddyzt(-eta,lon,lat,0,shape(eta)[0],1,levels,areamap=areamap,mask='',maskopt='forcefit',timeanalysis='none'\
                     ,preferences=preferences,filters=filters,areaparms=areaparm,destdir='',physics='',diagnostics=False,pprint=False)
print("Saving Negative",outputfilenumber)
save(outfile+'2layer_{0:05}_{1}_neg.npy'.format(outputfilenumber,layer),eddytdn)
