import matplotlib
matplotlib.use('agg')
import sys
from netCDF4 import Dataset
import os
import cmocean as cm
from trackeddy.tracking import *
from trackeddy.datastruct import *
from trackeddy.geometryfunc import *
from trackeddy.physics import *
from numpy import *
import xarray as xr

outputfilenumber = int(sys.argv[1])
division_number  = int(sys.argv[2])
file_division    = int(sys.argv[3])
file_count       = int(sys.argv[4])
outfile          = sys.argv[5]

outfolder='/scratch/x77/jm5970/trackeddy_output/post-processing/'

expts=['','_cyc','_acyc','_diff']
varname=['reconstruct','cyc','acyc','reconstruct']

#expts=['_cyc','_acyc']
#varname=['cyc','acyc']

def split_list(alist, wanted_parts=1):
    length = len(alist)
    return np.array([ alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
             for i in range(wanted_parts) ])

# Output data path
outputpath='/g/data/cj50/access-om2/raw-output/access-om2-01/01deg_jra55v140_iaf/output%03d/' % outputfilenumber

model_ssh=xr.open_mfdataset(outputpath+'ocean/ocean-2d-sea_level-1-daily-mean-ym_*.nc',combine='by_coords')
time=model_ssh.time.values[:]

time_division=split_list(range(0,len(time)), wanted_parts=file_division)

init_time= datetime.strptime(str(time[time_division[division_number][0]]), "%Y-%m-%d %H:%M:%S")

for ii in range(0,len(expts)):
   # Output data path
   outputfile=outfolder+'reconstructed_field_{0:05}_{1:02}{2}.nc'.format(outputfilenumber,division_number,expts[ii])
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
       u_eddy[tt,:,:],v_eddy[tt,:,:]=geovelfield(reconstruct[tt,:,:],lon,lat,mask,100000)
       EKE_eddy[tt,:,:] = KE(u_eddy[tt,:,:],v_eddy[tt,:,:])

   filename=outfolder+'EKE_eddy_{0:05}_{1:02}{2}.nc'.format(outputfilenumber,division_number,expts[ii])
   vargeonc(filename,lat,lon,EKE_eddy,shape(EKE_eddy)[0],'EKE_eddy',init_time,nc_description='EKE_eddy using the geostrophic velocity form the reconstructed field (Trackeddy).',units='m2/s2',dt='',dim='2D')
   
   filename=outfolder+'v_eddy_{0:05}_{1:02}{2}.nc'.format(outputfilenumber,division_number,expts[ii])
   vargeonc(filename,lat,lon,u_eddy,shape(EKE_eddy)[0],'v_eddy',init_time,nc_description='Geostrophic velocity form the reconstructed field (Trackeddy).',units='m/s',dt='',dim='2D')
   
   filename=outfolder+'u_eddy_{0:05}_{1:02}{2}.nc'.format(outputfilenumber,division_number,expts[ii])
   vargeonc(filename,lat,lon,v_eddy,shape(EKE_eddy)[0],'v_eddy',init_time,nc_description='Geostrophic velocity form the reconstructed field (Trackeddy).',units='m/s',dt='',dim='2D')


plt.pcolormesh(lon,lat,np.nanmean(EKE_eddy,axis=0),cmap=cm.cm.amp)
plt.colorbar()
plt.savefig(outfolder+'../figures/ke_{0:05}_{1:02}{2}.png'.format(outputfilenumber,division_number,expts[ii]))
plt.close()

eta=model_ssh.sea_level.values[time_division[division_number][0]:time_division[division_number][-1]+1,:,:]

u_eddy=np.zeros(np.shape(reconstruct))
v_eddy=np.zeros(np.shape(reconstruct))

for tt in range(0,np.shape(eta)[0]):
    u_eddy[tt,:,:],v_eddy[tt,:,:]=geovelfield(eta[tt,:,:],lon,lat,mask,100000)
    EKE_eddy[tt,:,:] = KE(u_eddy[tt,:,:],v_eddy[tt,:,:])


filename=outfolder+'KE_ACCESS_OM2_geostrophic_u_{0:05}_{1:02}.nc'.format(outputfilenumber,division_number)
vargeonc(filename,lat,lon,u_eddy,shape(EKE_eddy)[0],'u_eddy',init_time, nc_description='Geostrophic u (ACCESS-OM2).',units='m/s',dt='',dim='2D')

filename=outfolder+'KE_ACCESS_OM2_geostrophic_v_{0:05}_{1:02}.nc'.format(outputfilenumber,division_number)
vargeonc(filename,lat,lon,v_eddy,shape(EKE_eddy)[0],'v_eddy',init_time, nc_description='Geostrophic v (ACCESS-OM2).',units='m/s',dt='',dim='2D')

filename=outfolder+'KE_ACCESS_OM2_geostrophic_{0:05}_{1:02}.nc'.format(outputfilenumber,division_number)
vargeonc(filename,lat,lon,EKE_eddy,shape(EKE_eddy)[0],'KE_eddy',init_time, nc_description='Geostrophic kinetic energy (ACCESS-OM2).',units='m2/s2',dt='',dim='2D')
