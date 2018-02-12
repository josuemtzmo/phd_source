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
outfolder='/g/data/v45/jm5970/trackeddy_out/files_feb_incomplete/'

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
analysedatan=np.load(outfolder+outputfilenumber+'_neg.npy')

dictanalysep=analysedatap.item()
dictanalysen=analysedatan.item()

reconstruct_p=reconstruct_syntetic(etashape,lon,lat,dictanalysep)
reconstruct_n=reconstruct_syntetic(etashape,lon,lat,dictanalysen)

reconstruct=reconstruct_p+reconstruct_n

plt.pcolormesh(lon,lat,reconstruct[0,:,:])
plt.savefig(outfolder+'output/reconstructed_field_'+outputfilenumber+'.png')

filename=outfolder+'output/reconstructed_field_'+outputfilenumber+'.nc'
vargeonc(filename,lat,lon,reconstruct,shape(reconstruct)[0],'SSHa_reconstruct',nc_description='Reconstructed Field from SSHa field using Trackeddy.',units='m',dt='',dim='2D')
