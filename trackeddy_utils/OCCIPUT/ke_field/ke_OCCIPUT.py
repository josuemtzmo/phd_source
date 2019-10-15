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
from scipy.interpolate import griddata

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

ssh=ncfile.variables['ssh'][time_division[division_number][0]:time_division[division_number][-1]+1,:,:]

# Import geographic coor#dinates (Lon,Lat)
lon=ncfile.variables['nav_lon'][:]
lat=ncfile.variables['nav_lat'][:]

x=np.linspace(-180,180,shape(lon)[1])
y=np.linspace(-90,90,shape(lon)[0])
X,Y=meshgrid(x,y)

ncfile=Dataset('/g/data/v45/jm5970/trackeddy_output/OCCIPUT/pre-processing/ORCA025.L75-OCCITENS.{0:03}_y_mean.nc'.format(ensemble))
ssh_mean=squeeze(ncfile.variables['ssh'][:,:]).data

ssh_i=np.zeros((shape(ssh)[0],len(y),len(x)))
eta=np.zeros((shape(ssh)[0],len(y),len(x)))

transient_u=zeros(np.shape(eta))
transient_v=zeros(np.shape(eta))
transient_KE=zeros(np.shape(eta))

for t in range(shape(ssh)[0]):
    if os.path.isfile((outfolder+'ssh_interp_field_{0:03}.nc').format(file_count)):
        ncfile=Dataset((outfolder+'ssh_interp_field_{0:03}.nc').format(file_count))
        ssh_i[t,:,:]=squeeze(ncfile.variables['ssh'][t,:,:])
    else:
    	ssh_i[t,:,:]=griddata((lon.ravel(),lat.ravel()),ssh[t,:,:].ravel(),(X,Y),'linear')
    eta[t,:,:]=ssh_i[t,:,:]-ssh_mean
    mask=ma.getmask(eta[0,:,:])
    transient_u[t,:,:],transient_v[t,:,:]=geovelfield(eta[t,:,:],x,y,mask,5)
    transient_KE[t,:,:] = KE(transient_u[t,:,:]*100,transient_v[t,:,:]*100)

filename=(outfolder+'ssh_interp_field_{0:03}.nc').format(file_count)
vargeonc(filename,y,x,ssh_i,shape(ssh_i)[0],'ssh',init_time,nc_description='SSH field.',units='m',dt='',dim='2D')

filename=(outfolder+'ssha_field_{0:03}.nc').format(file_count)
vargeonc(filename,y,x,eta,shape(eta)[0],'ssha',init_time,nc_description='SSHa field.',units='m',dt='',dim='2D')

filename=(outfolder+'TKE_field_{0:03}.nc').format(file_count)
vargeonc(filename,y,x,transient_KE,shape(transient_KE)[0],'EKE_eddy',init_time,nc_description='TKE from SSHa field.',units='m2/s2',dt='',dim='2D')

filename=(outfolder+'transient_u_{0:03}.nc').format(file_count)
vargeonc(filename,y,x,transient_u,shape(transient_u)[0],'u',init_time,nc_description='OCCIPUT geostrophic velocity.',units='m/s',dt='',dim='2D')

filename=(outfolder+'transient_v_{0:03}.nc').format(file_count)
vargeonc(filename,y,x,transient_v,shape(transient_v)[0],'v',init_time,nc_description='OCCIPUT geostrophic velocity.',units='m/s',dt='',dim='2D')


expts=['']#,'_cyc','_acyc']
varname=['reconstruct']#,'cyc','acyc']

for ii in range(0,len(expts)):
   # Output data path
   if expts[ii]=='':
      outputfile=outfolder+'reconstructed_ssh_{0:03}.nc'.format(file_count)
   else:
      outputfile=outfolder+'reconstructed_ssh_{0:03}{1}.nc'.format(file_count,expts[ii])
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
       EKE_eddy[tt,:,:] = KE(u_eddy[tt,:,:]*100,v_eddy[tt,:,:]*100)
       EKE_res[tt,:,:] = KE((transient_u[tt,:,:]*100-u_eddy[tt,:,:]*100),(transient_v[tt,:,:]*100-v_eddy[tt,:,:]*100))
#   plt.pcolormesh(lon,lat,EKE_eddy[0,:,:])
#   plt.savefig(outfolder+'ke_'+year+'_'+str(monthsin)+'_'+str(monthsend)+'.png')

   filename=outfolder+'TEKE_field_{0:03}{1}.nc'.format(file_count,expts[ii])
   vargeonc(filename,lat,lon,EKE_eddy,shape(EKE_eddy)[0],'EKE_eddy',init_time,nc_description='EKE_eddy using the geostrophic velocity form the reconstructed field (Trackeddy).',units='cm2/s2',dt='',dim='2D')

   filename=outfolder+'v_eddy_field_{0:03}{1}.nc'.format(file_count,expts[ii])
   vargeonc(filename,lat,lon,v_eddy,shape(v_eddy)[0],'v_eddy',init_time,nc_description='Geostrophic velocity form the reconstructed field (Trackeddy).',units='m/s',dt='',dim='2D')

   filename=outfolder+'u_eddy_field_{0:03}{1}.nc'.format(file_count,expts[ii])
   vargeonc(filename,lat,lon,u_eddy,shape(u_eddy)[0],'u_eddy',init_time,nc_description='Geostrophic velocity form the reconstructed field (Trackeddy).',units='m/s',dt='',dim='2D')

   filename=outfolder+'TRKE_field_{0:03}{1}.nc'.format(file_count,expts[ii])
   vargeonc(filename,lat,lon,EKE_res,shape(EKE_res)[0],'EKE_res',init_time,nc_description='EKE_eddy using the geostrophic velocity form the reconstructed field (Trackeddy).',units='cm2/s2',dt='',dim='2D')

   filename=outfolder+'v_res_field_{0:03}{1}.nc'.format(file_count,expts[ii])
   vargeonc(filename,lat,lon,transient_v-v_eddy,shape(transient_v-v_eddy)[0],'v_res',init_time,nc_description='Residual Geostrophic velocity OCCIPUT - reconstructed field (Trackeddy).',units='m/s',dt='',dim='2D')

   filename=outfolder+'u_res_field_{0:03}{1}.nc'.format(file_count,expts[ii])
   vargeonc(filename,lat,lon,transient_u-u_eddy,shape(transient_u-u_eddy)[0],'u_res',init_time,nc_description='Residual Geostrophic velocity OCCIPUT - reconstructed field (Trackeddy).',units='m/s',dt='',dim='2D')

del transient_u,transient_v,EKE_eddy


# Cross terms
outputfile=outfolder+'v_eddy_field_{0:03}.nc'.format(file_count)
ncfile=Dataset(outputfile)
v_eddy=ncfile.variables['v_eddy'][:]

outputfile=outfolder+'u_eddy_field_{0:03}.nc'.format(file_count)
ncfile=Dataset(outputfile)
u_eddy=ncfile.variables['u_eddy'][:]

outputfile=outfolder+'v_res_field_{0:03}.nc'.format(file_count)
ncfile=Dataset(outputfile)
v_diff=ncfile.variables['v_res'][:]

outputfile=outfolder+'u_res_field_{0:03}.nc'.format(file_count)
ncfile=Dataset(outputfile)
u_diff=ncfile.variables['u_res'][:]

lon=ncfile.variables['lon'][:]
lat=ncfile.variables['lat'][:]

cross_EKE= 2*((u_eddy*100*u_diff*100)+(v_eddy*100*v_diff*100))

filename=outfolder+'TRKE_cross_field_{0:03}{1}.nc'.format(file_count,'_cross')
vargeonc(filename,lat,lon,cross_EKE,shape(cross_EKE)[0],'TEKE_c',init_time,nc_description='TRKE_c using the geostrophic velocity form the reconstructed field (Trackeddy).',units='cm2/s2',dt='',dim='2D')
