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

file_count       = int(sys.argv[1])
outputfilenumber = int(sys.argv[1])
expt = sys.argv[2]
level = int(sys.argv[3])

outfolder='/home/156/jm5970/data/trackeddy_output/simple_ocean_w_ridges/{0}/'.format(expt)

# Output data path
outputpath='/home/552/nc3020/SOchanBcBtEddySat/layer2/{0}/archive/output{1:03}/'.format(expt,outputfilenumber)

# Import SSH values to python environment.
ncfile=Dataset(outputpath+'prog.nc')
time=ncfile.variables['Time'][:]

init_time=datetime.fromordinal(int(round(time[0])))

eta=ncfile.variables['e'][:,0,:,:]
etashape=shape(eta)

# Import geographic coordinates (Lon,Lat)
lon=ncfile.variables['xh'][:]
lat=ncfile.variables['yh'][:]

print(init_time)
# Output data patha
try:
   filepath = outfolder+'npy/2layer_{0:05}_{1}_pos.npy'.format(file_count,level)
   analysedatap=np.load(filepath,allow_pickle=True)
   dictanalysep=analysedatap.item()
   reconstruct_p=reconstruct_syntetic(etashape,lon,lat,dictanalysep)
   
   filename=outfolder+'post-processing/reconstructed_field_{0}_cyc.nc'.format(file_count)
   vargeonc(filename,lat,lon,reconstruct_p,shape(reconstruct_p)[0],'SSHa_cyc',init_time,nc_description='Cyclonic reconstructed Field from SSHa field using Trackeddy.',units='m',dt='',dim='2D')
except:
   pass

try:
   filepath = outfolder+'npy/2layer_{0:05}_{1}_neg.npy'.format(file_count,level)
   analysedatan=np.load(filepath,allow_pickle=True)
   dictanalysen=analysedatan.item()
   reconstruct_n=-reconstruct_syntetic(etashape,lon,lat,dictanalysen)

   filename=outfolder+'post-processing/reconstructed_field_{0}_acyc.nc'.format(file_count)
   vargeonc(filename,lat,lon,reconstruct_n,shape(reconstruct_n)[0],'SSHa_acyc',init_time,nc_description='Anticyclonic reconstructed Field from SSHa field using Trackeddy.',units='m',dt='',dim='2D')
except:
   pass

try:
   reconstruct=reconstruct_p+reconstruct_n
   plt.pcolormesh(lon,lat,reconstruct[0,:,:])
   plt.savefig(outfolder+'post-processing/reconstructed_field_{0}.png'.format(file_count))

   filename=outfolder+'post-processing/reconstructed_field_{0}.nc'.format(file_count)
   vargeonc(filename,lat,lon,reconstruct,shape(reconstruct)[0],'SSHa_reconstruct',init_time,nc_description='Reconstructed Field from SSHa field using Trackeddy.',units='m',dt='',dim='2D')
   
   filename=outfolder+'post-processing/reconstructed_field_{0}_diff.nc'.format(file_count)
   vargeonc(filename,lat,lon,eta-reconstruct,shape(reconstruct)[0],'SSHa_reconstruct',init_time,nc_description='Reconstructed Field from SSHa field using Trackeddy.',units='m',dt='',dim='2D')
except:
   pass
