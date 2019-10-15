import xarray as xr
import numpy as np
from scipy.interpolate import griddata
#from dask.distributed import Client

#c=Client()
#print(c)

path='/g/data1a/x77/amh157/OCCIPUT/SSH_ENSEMBLE_all/ORCA025.L75-OCCITENS.{0:03}-S/1d/'

output_path='/g/data/v45/jm5970/trackeddy_output/OCCIPUT/pre-processing/'

for ii in range(43,44):
    print((path+"ORCA025.L75-OCCITENS.{0:03}_y*.1d_SSH.nc").format(ii))
    data = xr.open_mfdataset((path+"ORCA025.L75-OCCITENS.{0:03}_y*.1d_SSH.nc").format(ii)).ssh
    mean_ssh=data.mean(dim="time_counter").compute()
    
    print(data.nav_lon.shape)
    if len(data.nav_lon.shape)==3:
        lat=data.nav_lat.isel(time_counter=0).values
        lon=data.nav_lon.isel(time_counter=0).values
    else:
        lon=data.nav_lon.values
        lat=data.nav_lat.values
    
    x=np.linspace(-180,180,np.shape(lon)[1])
    y=np.linspace(-90,90,np.shape(lon)[0])
    X,Y=np.meshgrid(x,y)
    print(mean_ssh.shape)
    
    interp_data=griddata((lon.ravel(),lat.ravel()),mean_ssh.values.ravel(),(X,Y),'linear')
    print('Data interpolated')
    mean_ssh['ssh']=(('y','x'), interp_data) 
    mean_ssh['nav_lat']=('y',y)
    mean_ssh['nav_lon']=('x',x)
    mean_ssh.ssh.to_netcdf(output_path+'ORCA025.L75-OCCITENS.{0:03}_y_mean.nc'.format(ii))
    del interp_data,y,x,mean_ssh

print("DONE!")    

