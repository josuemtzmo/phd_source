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
from calendar import monthrange

year=sys.argv[1]
monthsin=int(sys.argv[2])
monthsend=int(sys.argv[3])

print('Analizing the year ',year,'in the months[',monthsin,'-',monthsend,']')
inputfiles='/g/data/ua8/CMEMS_SeaLevel/v3-0/'+year+'/'

outputfilenumber=sys.argv[1]
outfolder='/g/data/v45/jm5970/trackeddy_out/'

datashapetime=0
for month in range(monthsin,monthsend):
    datashapetime=datashapetime+monthrange(int(year), month)[1]

# Import SSH values to python environment.
ncfile=Dataset(inputfiles+'dt_global_allsat_phy_l4_'+year+'0101_20170110.nc')
ssha=np.squeeze(ncfile.variables['sla'][:])
# Import geographic coordinates (Lon,Lat)
lon=ncfile.variables['longitude'][:]
lat=ncfile.variables['latitude'][:]

sshashape=[datashapetime,shape(ssha)[0],shape(ssha)[1]]

# Output data path
try: 
   analysedatap=np.load(outfolder+year+str(monthsin)+'-'+str(monthsend)+'_pos_satellite.npy')
   dictanalysep=analysedatap.item()
   reconstruct_p=reconstruct_syntetic(sshashape,lon,lat,dictanalysep)

   filename=outfolder+'output/satellite_reconstructed_field_'+outputfilenumber+'_'+str(monthsin)+'_'+str(monthsend)+'_cyc.nc'
   vargeonc(filename,lat,lon,reconstruct_p,shape(reconstruct_p)[0],'SSHa_cyc',nc_description='Cyclonic reconstructed Field from SSHa field using Trackeddy.',units='m',dt='',dim='2D')
except:
   pass

try:
   analysedatan=np.load(outfolder+year+str(monthsin)+'-'+str(monthsend)+'_neg_satellite.npy')
   dictanalysen=analysedatan.item()
   reconstruct_n=reconstruct_syntetic(sshashape,lon,lat,dictanalysen)

   filename=outfolder+'output/satellite_reconstructed_field_'+outputfilenumber+'_'+str(monthsin)+'_'+str(monthsend)+'_acyc.nc'
   vargeonc(filename,lat,lon,reconstruct_n,shape(reconstruct_n)[0],'SSHa_acyc',nc_description='Anticyclonic reconstructed Field from SSHa field using Trackeddy.',units='m',dt='',dim='2D')
except:
   pass

try:
   reconstruct=reconstruct_p+reconstruct_n

   plt.pcolormesh(lon,lat,reconstruct[0,:,:])
   plt.savefig(outfolder+'output/satellite_reconstructed_field_'+outputfilenumber+'.png')

   filename=outfolder+'output/satellite_reconstructed_field_'+outputfilenumber+'_'+str(monthsin)+'_'+str(monthsend)+'.nc'
   vargeonc(filename,lat,lon,reconstruct,shape(reconstruct)[0],'SSHa_reconstruct',nc_description='Reconstructed Field from SSHa field using Trackeddy.',units='m',dt='',dim='2D')

   filename=outfolder+'output/satellite_reconstructed_field_'+outputfilenumber+'_'+str(monthsin)+'_'+str(monthsend)+'_diff.nc'
   vargeonc(filename,lat,lon,ssha-reconstruct,shape(reconstruct)[0],'SSHa_reconstruct',nc_description='Reconstructed Field from SSHa field using Trackeddy.',units='m',dt='',dim='2D')
except:
   pass
#mask=ma.getmask(ncfile.variables['eta_t'][0,:,:])

#u_eddy,v_eddy=geovelfield(reconstruct,lon,lat,mask,5)

#EKE_eddy = KE(u_eddy,v_eddy)

#filename=outfolder+'output/EKE_eddy'+outputfilenumber+'.nc'
#vargeonc(filename,lat,lon,reconstruct,shape(reconstruct)[0],'EKE_eddy',nc_description='EKE_eddy using the  geostrophic velocity form the reconstructed field (Trackeddy).',units='m',dt='',dim='2D')

