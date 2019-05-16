import xarray as xr

path='/g/data1a/x77/amh157/OCCIPUT/SSH_ENSEMBLE_all/ORCA025.L75-OCCITENS.{0:03}-S/1d/'

output_path='/g/data/v45/jm5970/trackeddy_output/OCCIPUT/pre-processing/'

for ii in range(43,51):#50):
    print((path+"ORCA025.L75-OCCITENS.{0:03}_y*.1d_SSH.nc").format(ii))
    data = xr.open_mfdataset((path+"ORCA025.L75-OCCITENS.{0:03}_y*.1d_SSH.nc").format(ii))
    mean_ssh=data.ssh.mean(dim="time_counter").compute()
    mean_ssh.to_netcdf(output_path+'ORCA025.L75-OCCITENS.{0:03}_y_mean.nc'.format(ii))

print("DONE!")    

