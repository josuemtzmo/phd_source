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
#from trackeddy.plotfunc import *
from numpy import *
from calendar import monthrange
import gsw as gs
import datetime
import xarray as xr

from os import listdir
from os.path import isfile, join

year=sys.argv[1]
outputfilenumber=sys.argv[1]
index_files=int(sys.argv[2])
divisions=int(sys.argv[3])


outfolder='/g/data/v45/jm5970/trackeddy_output/AVISO+/post-processing/'

inputfiles='/g/data/ua8/CMEMS_SeaLevel/v4-0/'+year+'/'

onlyfiles = [join(inputfiles, f) for f in listdir(inputfiles) if isfile(join(inputfiles, f))]

onlyfiles.sort()

def split_list(alist, wanted_parts=1):
    length = len(alist)
    return np.array([ alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
             for i in range(wanted_parts) ])

files2analyse=split_list(onlyfiles, divisions)

print('Analizing the year ',year,'from file ',files2analyse[index_files][0],'-',files2analyse[index_files][-1],']')

data=xr.open_mfdataset(files2analyse[index_files])
ssha=data.sla.values
lon=data.longitude.values
lat=data.latitude.values

init_time=datetime.datetime.strptime(str(data.time.isel(time=0).values).split('T')[0], "%Y-%m-%d")


sat_EKE=KE(data.ugosa.squeeze().values,data.vgosa.squeeze().values)
sat_u=data.ugosa.squeeze().values
sat_v=data.vgosa.squeeze().values

filename='{0}satellite_EKE_field_{1}_{2:03}.nc'.format(outfolder,outputfilenumber,index_files)
vargeonc(filename,lat,lon,sat_EKE,shape(sat_EKE)[0],'EKE_eddy',init_time,nc_description='EKE from SSHa field.',units='m',dt='',dim='2D')

filename='{0}satellite_u_{1}_{2:03}.nc'.format(outfolder,outputfilenumber,index_files)
vargeonc(filename,lat,lon,sat_u,shape(sat_u)[0],'u',init_time,nc_description='Geostrophic velocity Aviso +.',units='m/s',dt='',dim='2D')
   
filename='{0}satellite_v_{1}_{2:03}.nc'.format(outfolder,outputfilenumber,index_files)
vargeonc(filename,lat,lon,sat_v,shape(sat_v)[0],'v',init_time,nc_description='Geostrophic velocity Aviso +.',units='m/s',dt='',dim='2D')

expts=['','_cyc','_acyc','_diff']
varname=['reconstruct','cyc','acyc','reconstruct']

#expts=['_cyc','_acyc']
#varname=['cyc','acyc']

for ii in range(0,len(expts)):
   # Output data path
   outputfile='{0}satellite_reconstructed_field_{1}_{2:03}{3}.nc'.format(outfolder,outputfilenumber,index_files,expts[ii])
   # Import SSH values to python environment.
   ncfile=Dataset(outputfile)
   reconstruct=ncfile.variables['SSHa_'+varname[ii]][:]
   # Import geographic coordinates (Lon,Lat)
   lon=ncfile.variables['lon'][:]
   lat=ncfile.variables['lat'][:]
   
   # Output data path
   mask=ma.getmask(reconstruct[0,:,:])
   EKE_eddy=np.zeros(np.shape(reconstruct))
   EKE_res=np.zeros(np.shape(reconstruct))
   u_eddy=np.zeros(np.shape(reconstruct))
   v_eddy=np.zeros(np.shape(reconstruct))

   for tt in range(0,np.shape(reconstruct)[0]):
       u_eddy[tt,:,:],v_eddy[tt,:,:]=geovelfield(reconstruct[tt,:,:],lon,lat,mask,5)
       EKE_eddy[tt,:,:] = KE(u_eddy[tt,:,:],v_eddy[tt,:,:])
       EKE_res[tt,:,:] = KE((sat_u[tt,:,:]-u_eddy[tt,:,:]),(sat_v[tt,:,:]-v_eddy[tt,:,:]))
#   plt.pcolormesh(lon,lat,EKE_eddy[0,:,:])
#   plt.savefig(outfolder+'ke_'+year+'_'+str(monthsin)+'_'+str(monthsend)+'.png')
   filename='{0}satellite_TEKE_eddy_{1}_{2:03}{3}.nc'.format(outfolder,outputfilenumber,index_files,expts[ii])
   vargeonc(filename,lat,lon,EKE_eddy,shape(EKE_eddy)[0],'EKE_eddy',init_time,nc_description='EKE_eddy using the geostrophic velocity form the reconstructed field (Trackeddy).',units='cm2/s2',dt='',dim='2D')
   
   filename='{0}satellite_v_eddy_{1}_{2:03}{3}.nc'.format(outfolder,outputfilenumber,index_files,expts[ii])
   vargeonc(filename,lat,lon,v_eddy,shape(v_eddy)[0],'v_eddy',init_time,nc_description='Geostrophic velocity form the reconstructed field (Trackeddy).',units='m/s',dt='',dim='2D')
   
   filename='{0}satellite_u_eddy_{1}_{2:03}{3}.nc'.format(outfolder,outputfilenumber,index_files,expts[ii])
   vargeonc(filename,lat,lon,u_eddy,shape(u_eddy)[0],'u_eddy',init_time,nc_description='Geostrophic velocity form the reconstructed field (Trackeddy).',units='m/s',dt='',dim='2D')

   filename='{0}satellite_TEKE_res_{1}_{2:03}{3}.nc'.format(outfolder,outputfilenumber,index_files,expts[ii])
   vargeonc(filename,lat,lon,EKE_res,shape(EKE_res)[0],'EKE_res',init_time,nc_description='EKE_eddy using the geostrophic velocity form the reconstructed field (Trackeddy).',units='cm2/s2',dt='',dim='2D')

   filename='{0}satellite_v_residual_{1}_{2:03}{3}.nc'.format(outfolder,outputfilenumber,index_files,expts[ii])
   vargeonc(filename,lat,lon,sat_v-v_eddy,shape(sat_v-v_eddy)[0],'v_res',init_time,nc_description='Residual Geostrophic velocity Aviso+ - reconstructed field (Trackeddy).',units='m/s',dt='',dim='2D')

   filename='{0}satellite_u_residual_{1}_{2:03}{3}.nc'.format(outfolder,outputfilenumber,index_files,expts[ii])
   vargeonc(filename,lat,lon,sat_u-u_eddy,shape(sat_u-u_eddy)[0],'u_res',init_time,nc_description='Residual Geostrophic velocity Aviso+ - reconstructed field (Trackeddy).',units='m/s',dt='',dim='2D')

del u_eddy,v_eddy,sat_u,sat_v,EKE_eddy

# Cross terms
outputfile='{0}satellite_v_eddy_{1}_{2:03}{3}.nc'.format(outfolder,outputfilenumber,index_files,expts[ii])
ncfile=Dataset(outputfile)
v_eddy=ncfile.variables['v_eddy'][:]

outputfile='{0}satellite_u_eddy_{1}_{2:03}{3}.nc'.format(outfolder,outputfilenumber,index_files,expts[ii])
ncfile=Dataset(outputfile)
u_eddy=ncfile.variables['u_eddy'][:]

outputfile='{0}satellite_v_residual_{1}_{2:03}{3}.nc'.format(outfolder,outputfilenumber,index_files,expts[ii])
ncfile=Dataset(outputfile)
v_diff=ncfile.variables['v_res'][:]

outputfile='{0}satellite_u_residual_{1}_{2:03}{3}.nc'.format(outfolder,outputfilenumber,index_files,expts[ii])
ncfile=Dataset(outputfile)
u_diff=ncfile.variables['u_res'][:]

lon=ncfile.variables['lon'][:]
lat=ncfile.variables['lat'][:]

cross_EKE= 2*((u_eddy*u_diff)+(v_eddy*v_diff))

filename='{0}satellite_TEKE_cross_{1}_{2:03}{3}.nc'.format(outfolder,outputfilenumber,index_files,expts[ii])
vargeonc(filename,lat,lon,cross_EKE,shape(cross_EKE)[0],'TEKE_c',init_time,nc_description='EKE_eddy using the geostrophic velocity form the reconstructed field (Trackeddy).',units='cm2/s2',dt='',dim='2D')

