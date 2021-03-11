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
from numpy import *

import xarray as xr


outputfilenumber = int(sys.argv[1])
division_number  = int(sys.argv[2])
file_division    = int(sys.argv[3])
file_count       = int(sys.argv[4])
outfile          = sys.argv[5]

def split_list(alist, wanted_parts=1):
    length = len(alist)
    return np.array([ alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
             for i in range(wanted_parts) ])

outfolder='/scratch/x77/jm5970/trackeddy_output/'

# Output data path
outputpath='/g/data/cj50/access-om2/raw-output/access-om2-01/01deg_jra55v140_iaf/output%03d/' % outputfilenumber

# Import SSH values to python environment.
ncfile=xr.open_mfdataset(outputpath+'ocean/ocean-2d-sea_level-1-daily-mean-ym_*.nc',combine='by_coords')
time=ncfile.time.values[:]

time_division=split_list(range(0,len(time)), wanted_parts=file_division)

init_time= datetime.strptime(str(time[time_division[division_number][0]]), "%Y-%m-%d %H:%M:%S")

eta_access=ncfile.sea_level.values[time_division[division_number][0]:time_division[division_number][-1]+1,:,:]
etashape=shape(eta_access)

eta_mean=xr.open_dataset('/g/data/v45/jm5970/trackeddy_output/ACCESS_OM2-01/pre-processing/ACCESS-OM2_01d_eta_mean.nc')
ssh_mean = eta_mean.sea_level.values

eta = eta_access - ssh_mean

# Import geographic coordinates (Lon,Lat)
lon=ncfile.xt_ocean.values[:]
lat=ncfile.yt_ocean.values[:]

print('Time: ',init_time)
print('Analysing files: ','ACCESS_01_{0:05}_{1:02}_*.npy'.format(outputfilenumber,division_number))

# Output data patha
filepath = outfolder+'npy/ACCESS_01_{0:05}_{1:02}_pos.npy'.format(outputfilenumber,division_number) 
analysedatap=np.load(filepath,allow_pickle=True)
dictanalysep=analysedatap.item()
reconstruct_p=reconstruct_syntetic(etashape,lon,lat,dictanalysep)

filename=outfolder+'post-processing/reconstructed_field_{0:05}_{1:02}_cyc.nc'.format(outputfilenumber,division_number)
vargeonc(filename,lat,lon,reconstruct_p,shape(reconstruct_p)[0],'SSHa_cyc',init_time,nc_description='Cyclonic reconstructed Field from SSHa field using Trackeddy.',units='m',dt='',dim='2D')
#pos_pd = dict2pd(dictanalysep,inittime=init_time.strftime("%d-%m-%Y"),n=0,polarity='pos',ensemble=None)
reconstruct_p = xr.open_dataset(filename).SSHa_cyc

filepath = outfolder+'npy/ACCESS_01_{0:05}_{1:02}_neg.npy'.format(outputfilenumber,division_number) 
analysedatan=np.load(filepath,allow_pickle=True)
dictanalysen=analysedatan.item()
reconstruct_n=-reconstruct_syntetic(etashape,lon,lat,dictanalysen)

filename=outfolder+'post-processing/reconstructed_field_{0:05}_{1:02}_acyc.nc'.format(outputfilenumber,division_number)
vargeonc(filename,lat,lon,reconstruct_n,shape(reconstruct_n)[0],'SSHa_acyc',init_time,nc_description='Anticyclonic reconstructed Field from SSHa field using Trackeddy.',units='m',dt='',dim='2D')
#neg_pd = dict2pd(dictanalysen,inittime=init_time.strftime("%d-%m-%Y"),n=0,polarity='neg',ensemble=None)
reconstruct_n = xr.open_dataset(filename).SSHa_acyc

reconstruct = (reconstruct_p + reconstruct_n).values
plt.pcolormesh(lon,lat,reconstruct[0,:,:])
plt.colorbar()
plt.savefig(outfolder+'figures/reconstructed_field_{0:05}_{1:02}.png'.format(outputfilenumber,division_number))

filename=outfolder+'post-processing/reconstructed_field_{0:05}_{1:02}.nc'.format(outputfilenumber,division_number)
vargeonc(filename,lat,lon,reconstruct,shape(reconstruct)[0],'SSHa_reconstruct',init_time,nc_description='Reconstructed Field from SSHa field using Trackeddy.',units='m',dt='',dim='2D')
   
filename=outfolder+'post-processing/reconstructed_field_{0:05}_{1:02}_diff.nc'.format(outputfilenumber,division_number)
vargeonc(filename,lat,lon,eta-reconstruct,shape(reconstruct)[0],'SSHa_reconstruct',init_time,nc_description='Reconstructed Field from SSHa field using Trackeddy.',units='m',dt='',dim='2D')

#pd_result = pd.concat([pos_pd,neg_pd])
#pd_result.to_csv(outfolder+'pandas/csv_identified_eddies_{0:05}_{1:02}.csv'.format(outputfilenumber,division_number))
