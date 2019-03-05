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
outfolder='/g/data/v45/jm5970/trackeddy_output/ACCESS_OM2/post-processing/'

expts=['','_cyc','_acyc']
varname=['reconstruct','cyc','acyc']

#expts=['_cyc','_acyc']
#varname=['cyc','acyc']

for ii in range(0,len(expts)):
   # Output data path
   if expts[ii]=='':
      outputfile=outfolder+'reconstructed_field_'+outputfilenumber+'.nc'
   else:
      outputfile=outfolder+'reconstructed_field_'+outputfilenumber+expts[ii]+'.nc'
   # Import SSH values to python environment.
   ncfile=Dataset(outputfile)
   reconstruct=ncfile.variables['SSHa_'+varname[ii]][:]
   # Import geographic coordinates (Lon,Lat)
   lon=ncfile.variables['lon'][:]
   lat=ncfile.variables['lat'][:]
   
   # Output data path
   mask=ma.getmask(reconstruct[0,:,:])
   EKE_eddy=np.zeros(np.shape(reconstruct))
   u_eddy=np.zeros(np.shape(reconstruct))
   v_eddy=np.zeros(np.shape(reconstruct))

   for tt in range(0,np.shape(reconstruct)[0]):
       u_eddy[tt,:,:],v_eddy[tt,:,:]=geovelfield(reconstruct[tt,:,:],lon,lat,mask,100)
       EKE_eddy[tt,:,:] = KE(u_eddy[tt,:,:],v_eddy[tt,:,:])

   plt.pcolormesh(lon,lat,EKE_eddy[0,:,:])
   plt.savefig(outfolder+'ke_'+outputfilenumber+'.png')

   filename=outfolder+'EKE_eddy'+outputfilenumber+expts[ii]+'.nc'
   vargeonc(filename,lat,lon,EKE_eddy,shape(EKE_eddy)[0],'EKE_eddy',nc_description='EKE_eddy using the geostrophic velocity form the reconstructed field (Trackeddy).',units='m2/s2',dt='',dim='2D')
   
   filename=outfolder+'v_eddy'+outputfilenumber+expts[ii]+'.nc'
   vargeonc(filename,lat,lon,u_eddy,shape(EKE_eddy)[0],'v_eddy',nc_description='Geostrophic velocity form the reconstructed field (Trackeddy).',units='m/s',dt='',dim='2D')
   
   filename=outfolder+'u_eddy'+outputfilenumber+expts[ii]+'.nc'
   vargeonc(filename,lat,lon,v_eddy,shape(EKE_eddy)[0],'v_eddy',nc_description='Geostrophic velocity form the reconstructed field (Trackeddy).',units='m/s',dt='',dim='2D')
