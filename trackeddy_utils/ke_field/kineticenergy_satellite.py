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

year=sys.argv[1]
monthsin=int(sys.argv[2])
monthsend=int(sys.argv[3])

print('Analizing the year ',year,'in the months[',monthsin,'-',monthsend,']')
outfolder='/g/data/v45/jm5970/trackeddy_out/output/'

expts=['','_cyc','_acyc']
varname=['reconstruct','cyc','acyc']

#expts=['_cyc','_acyc']
#varname=['cyc','acyc']

for ii in range(0,len(expts)):
   # Output data path
   if expts[ii]=='':
      outputfile=outfolder+'reconstructed_field_'+year+str(monthsin)+'-'+str(monthsend)+'.nc'
   else:
      outputfile=outfolder+'reconstructed_field_'+year+str(monthsin)+'-'+str(monthsend)+expts[ii]+'.nc'
   # Import SSH values to python environment.
   ncfile=Dataset(outputfile)
   reconstruct=ncfile.variables['SSHa_'+varname[ii]][:]
   # Import geographic coordinates (Lon,Lat)
   lon=ncfile.variables['lon'][:]
   lat=ncfile.variables['lat'][:]
   
   # Output data path
   mask=ma.getmask(reconstruct[0,:,:])
   EKE_eddy=np.zeros(np.shape(reconstruct))

   for tt in range(0,np.shape(reconstruct)[0]):
       u_eddy,v_eddy=geovelfield(reconstruct[tt,:,:],lon,lat,mask,5)
       EKE_eddy[tt,:,:] = KE(u_eddy,v_eddy)

   plt.pcolormesh(lon,lat,EKE_eddy[0,:,:])
   plt.savefig(outfolder+'ke_'+year+'_'+str(monthsin)+'_'+str(monthsend)+'.png')

   filename=outfolder+'EKE_eddy_'+year+'_'+str(monthsin)+'_'+str(monthsend)+expts[ii]+'.nc'
   vargeonc(filename,lat,lon,EKE_eddy,shape(EKE_eddy)[0],'EKE_eddy',nc_description='EKE_eddy using the geostrophic velocity form the reconstructed field (Trackeddy).',units='m',dt='',dim='2D')
   
   filename=outfolder+'v_eddy_'+year+'_'+str(monthsin)+'_'+str(monthsend)+expts[ii]+'.nc'
   vargeonc(filename,lat,lon,EKE_eddy,shape(EKE_eddy)[0],'v_eddy',nc_description='Geostrophic velocity form the reconstructed field (Trackeddy).',units='m',dt='',dim='2D')
   
   filename=outfolder+'u_eddy_'+year+'_'+str(monthsin)+'_'+str(monthsend)+expts[ii]+'.nc'
   vargeonc(filename,lat,lon,EKE_eddy,shape(EKE_eddy)[0],'v_eddy',nc_description='Geostrophic velocity form the reconstructed field (Trackeddy).',units='m',dt='',dim='2D')
