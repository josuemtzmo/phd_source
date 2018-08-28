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
outfolder='/g/data/v45/jm5970/trackeddy_out/'

# Output data path
outputpath='/g/data3/hh5/tmp/akm157/mom01v5_kds75/output'+outputfilenumber+'/'
# Import SSH values to python environment.
ncfile=Dataset(outputpath+'rregionsouthern_ocean_daily_eta_t.nc')
etashape=np.shape(ncfile.variables['eta_t'][:])
# Import geographic coordinates (Lon,Lat)
lon=ncfile.variables['xt_ocean_sub01'][:]
lat=ncfile.variables['yt_ocean_sub01'][:]

# Output data path
analysedatap=np.load(outfolder+outputfilenumber+'_pos.npy')
dictanalysep=analysedatap.item()
reconstruct_p=reconstruct_syntetic(etashape,lon,lat,dictanalysep)

filename=outfolder+'output/reconstructed_field_'+outputfilenumber+'_cyc.nc'
vargeonc(filename,lat,lon,reconstruct_p,shape(reconstruct_p)[0],'SSHa_cyc',nc_description='Cyclonic reconstructed Field from SSHa field using Trackeddy.',units='m',dt='',dim='2D')

analysedatan=np.load(outfolder+outputfilenumber+'_neg.npy')
dictanalysen=analysedatan.item()
reconstruct_n=reconstruct_syntetic(etashape,lon,lat,dictanalysen)

filename=outfolder+'output/reconstructed_field_'+outputfilenumber+'_acyc.nc'
vargeonc(filename,lat,lon,reconstruct_n,shape(reconstruct_n)[0],'SSHa_acyc',nc_description='Anticyclonic reconstructed Field from SSHa field using Trackeddy.',units='m',dt='',dim='2D')

reconstruct=reconstruct_p+reconstruct_n

plt.pcolormesh(lon,lat,reconstruct[0,:,:])
plt.savefig(outfolder+'output/reconstructed_field_'+outputfilenumber+'.png')

filename=outfolder+'output/reconstructed_field_'+outputfilenumber+'.nc'
vargeonc(filename,lat,lon,reconstruct,shape(reconstruct)[0],'SSHa_reconstruct',nc_description='Reconstructed Field from SSHa field using Trackeddy.',units='m',dt='',dim='2D')

#mask=ma.getmask(ncfile.variables['eta_t'][0,:,:])

#u_eddy,v_eddy=geovelfield(reconstruct,lon,lat,mask,5)

#EKE_eddy = KE(u_eddy,v_eddy)

#filename=outfolder+'output/EKE_eddy'+outputfilenumber+'.nc'
#vargeonc(filename,lat,lon,reconstruct,shape(reconstruct)[0],'EKE_eddy',nc_description='EKE_eddy using the  geostrophic velocity form the reconstructed field (Trackeddy).',units='m',dt='',dim='2D')

