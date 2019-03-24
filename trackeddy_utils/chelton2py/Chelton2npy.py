from pylab import *
from netCDF4 import Dataset
import xarray as xr
import numpy as np

path='/g/data/v45/jm5970/data.input/eddies_database/'
files=['eddy_trajectory_2.0exp_19930101_20180118.nc']

fpath = path + files[0]

process=int(sys.argv[1])
totproc=int(sys.argv[2])

def split_list(alist, wanted_parts=1):
    length = len(alist)
    return np.array([ alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
             for i in range(wanted_parts) ])

def chelton2trackeddy(path,process,totproc):
    ncfile = xr.open_dataset(path,autoclose=True,decode_times=False)
    eddydt={}
    alist=squeeze(where(ncfile.observation_number==0))
    unique_idx=split_list(alist, wanted_parts=totproc)[process]
    print(len(unique_idx))
    fidx=zeros((len(unique_idx)+1),dtype=int)
    fidx[0:-1] =unique_idx
    if totproc-1 == process:
        fidx[-1] = len(ncfile.observation_number)
    else:
        fidx[-1] = split_list(alist, wanted_parts=totproc)[process+1][0]
    tneddies = len(unique_idx)
    for ii in range(tneddies):
        sys.stdout.write("\r\x1b[K"+str(ii).__str__())
        sys.stdout.flush()
        in0=fidx[ii]
        in1=fidx[ii+1]
        obs=np.array(ncfile.obs.isel(obs=slice(in0,in1)).values,dtype=float)
        time=np.array(ncfile.time.isel(obs=slice(in0,in1)).values,dtype=float)
        latitude=np.array(ncfile.latitude.isel(obs=slice(in0,in1)).values,dtype=float)
        longitude=np.array(ncfile.longitude.isel(obs=slice(in0,in1)).values,dtype=float)
        amplitude=np.array(ncfile.amplitude.isel(obs=slice(in0,in1)).values,dtype=float)
        position=np.vstack((longitude,latitude,amplitude))
        speed_radius=np.array(ncfile.speed_radius.isel(obs=slice(in0,in1)).values,dtype=float)
        eddydt['eddyn_%d'%ii]={'neddy':ii,'time':time,'position_default':[],'area':[],\
                              'ellipse':[],'contour':[],'angle':[],'position_maxvalue':[position],\
                              'position_eddy':[],'level':obs,'majoraxis':[],'minoraxis':[],\
                              '2dgaussianfit':[speed_radius,speed_radius],'timetracking':False}
    np.save(path.split('eddy_trajectory')[0]+'chelton_dataset_%03d.npy' %process, eddydt)
    return eddydt
