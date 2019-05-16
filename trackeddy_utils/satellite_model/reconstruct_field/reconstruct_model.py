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
import math

file_count       = sys.argv[1]
file_division    = 3
outputfilenumber = math.floor((int(file_count)/file_division)+1)
division_number  = outputfilenumber%int(file_division)

def split_list(alist, wanted_parts=1):
    length = len(alist)
    return np.array([ alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
             for i in range(wanted_parts) ])

outfolder='/g/data/v45/jm5970/trackeddy_output/ACCESS_OM2/'

# Output data path
outputpath='/g/data3/hh5/tmp/cosima/access-om2-01/01deg_jra55v13_iaf/output%03d/' % outputfilenumber
# Import SSH values to python environment.
ncfile=Dataset(outputpath+'ocean/ocean_daily.nc')
time=ncfile.variables['time'][:]

init_time=datetime.fromordinal(int(round(time[0])))

time_division=split_list(range(0,len(time)), wanted_parts=file_division)

eta=ncfile.variables['eta_t'][time_division[division_number][0]:time_division[division_number][-1]+1,:,:]
etashape=shape(eta)

# Import geographic coordinates (Lon,Lat)
lon=ncfile.variables['xt_ocean'][:]
lat=ncfile.variables['yt_ocean'][:]

print(init_time)
# Output data patha
try:
   filepath = outfolder+'npy/ACCESS_{0:05}_pos.npy'.format(int(file_count))
   analysedatap=np.load(filepath)
   dictanalysep=analysedatap.item()
   reconstruct_p=reconstruct_syntetic(etashape,lon,lat,dictanalysep)

   filename=outfolder+'post-processing/reconstructed_field_'+file_count+'_cyc.nc'
   vargeonc(filename,lat,lon,reconstruct_p,shape(reconstruct_p)[0],'SSHa_cyc',init_time,nc_description='Cyclonic reconstructed Field from SSHa field using Trackeddy.',units='m',dt='',dim='2D')
except:
   pass

try:
   filepath = outfolder+'npy/ACCESS_{0:05}_neg.npy'.format(int(file_count))
   analysedatan=np.load(filepath)
   dictanalysen=analysedatan.item()
   reconstruct_n=reconstruct_syntetic(etashape,lon,lat,dictanalysen)

   filename=outfolder+'post-processing/reconstructed_field_'+file_count+'_acyc.nc'
   vargeonc(filename,lat,lon,reconstruct_n,shape(reconstruct_n)[0],'SSHa_acyc',init_time,nc_description='Anticyclonic reconstructed Field from SSHa field using Trackeddy.',units='m',dt='',dim='2D')
except:
   pass

try:

   reconstruct=reconstruct_p+reconstruct_n
   plt.pcolormesh(lon,lat,reconstruct[0,:,:])
   plt.savefig(outfolder+'post-processing/reconstructed_field_'+file_count+'.png')

   filename=outfolder+'post-processing/reconstructed_field_'+file_count+'.nc'
   vargeonc(filename,lat,lon,reconstruct,shape(reconstruct)[0],'SSHa_reconstruct',init_time,nc_description='Reconstructed Field from SSHa field using Trackeddy.',units='m',dt='',dim='2D')
   
   filename=outfolder+'post-processing/reconstructed_field_'+file_count+'_diff.nc'
   vargeonc(filename,lat,lon,eta-reconstruct,shape(reconstruct)[0],'SSHa_reconstruct',init_time,nc_description='Reconstructed Field from SSHa field using Trackeddy.',units='m',dt='',dim='2D')
except:
   pass
#mask=ma.getmask(ncfile.variables['eta_t'][0,:,:])

#u_eddy,v_eddy=geovelfield(reconstruct,lon,lat,mask,5)

#EKE_eddy = KE(u_eddy,v_eddy)

#filename=outfolder+'output/EKE_eddy'+outputfilenumber+'.nc'
#vargeonc(filename,lat,lon,reconstruct,shape(reconstruct)[0],'EKE_eddy',nc_description='EKE_eddy using the  geostrophic velocity form the reconstructed field (Trackeddy).',units='m',dt='',dim='2D')

