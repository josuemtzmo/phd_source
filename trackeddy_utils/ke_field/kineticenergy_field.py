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
outfolder='/g/data/v45/jm5970/trackeddy_out/output/'

# Output data path
outputfile=outfolder+'reconstructed_field_'+outputfilenumber+'.nc'
# Import SSH values to python environment.
ncfile=Dataset(outputfile)
reconstruct=ncfile.variables['SSHa_reconstruct'][:]
# Import geographic coordinates (Lon,Lat)
lon=ncfile.variables['lon'][:]
lat=ncfile.variables['lat'][:]

# Output data path
mask=ma.getmask(reconstruct[0,:,:])
EKE_eddy=np.zeros(np.shape(reconstruct))

for tt in range(0,np.shape(reconstruct)[0]):
    u_eddy,v_eddy=geovelfield(reconstruct[tt,:,:],lon,lat,mask,100)
    EKE_eddy[tt,:,:] = KE(u_eddy,v_eddy)

plt.pcolormesh(lon,lat,EKE_eddy[0,:,:])
plt.savefig(outfolder+'ke_'+outputfilenumber+'.png')

filename=outfolder+'EKE_eddy'+outputfilenumber+'.nc'
vargeonc(filename,lat,lon,EKE_eddy,shape(EKE_eddy)[0],'EKE_eddy',nc_description='EKE_eddy using the  geostrophic velocity form the reconstructed field (Trackeddy).',units='m',dt='',dim='2D')

