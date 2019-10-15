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

ensemble = int(sys.argv[1])
year             =int(sys.argv[2])
file_division    =int(sys.argv[3])
division_number  =int(sys.argv[4])
file_count       =int(sys.argv[5])

def split_list(alist, wanted_parts=1):
    length = len(alist)
    return np.array([ alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
             for i in range(wanted_parts) ])


outfolder='/g/data/v45/jm5970/trackeddy_output/OCCIPUT/post-processing/ORCA025.L75-OCCITENS.{0:03}/'.format(ensemble)

try:
    os.mkdir(outfolder)
except:
    print('previous data overwritten')


outfile='/g/data/v45/jm5970/trackeddy_output/OCCIPUT/npy/ORCA025.L75-OCCITENS.{0:03}/'.format(ensemble)

# Output data path
outputpath='/g/data/x77/amh157/OCCIPUT/SSH_ENSEMBLE_all/ORCA025.L75-OCCITENS.%03d-S/' % ensemble
# Import SSH values to python environment.
ncfile=Dataset(outputpath+'1d/ORCA025.L75-OCCITENS.{0:03}_y{1}.1d_SSH.nc'.format(ensemble,year))
time=ncfile.variables['time_counter'][:]

time_division=split_list(range(0,len(time)), wanted_parts=file_division)

init_time=timedelta(int(round(time[time_division[division_number][0]]/(60*60*24)-365*2)))+datetime(1960,1,1)

etashape=np.shape(ncfile.variables['ssh'][time_division[division_number][0]:time_division[division_number][-1]+1,:,:])

# Import geographic coor#dinates (Lon,Lat)
lonshape=np.shape(ncfile.variables['nav_lon'][:])

x=np.linspace(-180,180,lonshape[1])
y=np.linspace(-90,90,lonshape[0])

print(init_time,etashape)
# Output data path
try:
  filepath = outfile+'OCCIPUT_{0:05}_pos.npy'.format(int(file_count))
  print(filepath)
  analysedatap=np.load(filepath)
  dictanalysep=analysedatap.item()
  reconstruct_p=reconstruct_syntetic(etashape,x,y,dictanalysep)

  filename=outfolder+'reconstructed_ssh_{0:03}_cyc.nc'.format(file_count)
  vargeonc(filename,y,x,reconstruct_p,shape(reconstruct_p)[0],'SSHa_cyc',init_time,nc_description='Cyclonic reconstructed Field from SSHa field using Trackeddy.',units='m',dt='',dim='2D')
except:
   pass

try:
   filepath = outfile+'OCCIPUT_{0:05}_neg.npy'.format(int(file_count))
   analysedatan=np.load(filepath)
   dictanalysen=analysedatan.item()
   reconstruct_n=reconstruct_syntetic(etashape,x,y,dictanalysen)

   filename=outfolder+'reconstructed_ssh_{0:03}_acyc.nc'.format(file_count)
   vargeonc(filename,y,x,reconstruct_n,shape(reconstruct_n)[0],'SSHa_acyc',init_time,nc_description='Anticyclonic reconstructed Field from SSHa field using Trackeddy.',units='m',dt='',dim='2D')
except:
   pass

try:

   reconstruct=reconstruct_p+reconstruct_n
   #plt.pcolormesh(x,y,reconstruct[0,:,:])
   #plt.savefig(outfolder+'reconstructed_field_'+file_count+'.png')

   filename=outfolder+'reconstructed_ssh_{0:03}.nc'.format(file_count)
   vargeonc(filename,y,x,reconstruct,shape(reconstruct)[0],'SSHa_reconstruct',init_time,nc_description='Reconstructed Field from SSHa field using Trackeddy.',units='m',dt='',dim='2D')
   
#   filename=outfolder+'reconstructed_ssh_{0:03}_diff.nc'.format(file_count)
#   vargeonc(filename,y,x,eta-reconstruct,shape(reconstruct)[0],'SSHa_reconstruct',init_time,nc_description='Reconstructed Field from SSHa field using Trackeddy.',units='m',dt='',dim='2D')
except:
   pass
#mask=ma.getmask(ncfile.variables['eta_t'][0,:,:])

#u_eddy,v_eddy=geovelfield(reconstruct,lon,lat,mask,5)

#EKE_eddy = KE(u_eddy,v_eddy)

#filename=outfolder+'output/EKE_eddy'+outputfilenumber+'.nc'
#vargeonc(filename,lat,lon,reconstruct,shape(reconstruct)[0],'EKE_eddy',nc_description='EKE_eddy using the  geostrophic velocity form the reconstructed field (Trackeddy).',units='m',dt='',dim='2D')

