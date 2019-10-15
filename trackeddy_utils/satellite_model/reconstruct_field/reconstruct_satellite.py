import matplotlib
matplotlib.use('agg')
import sys
import os
os.environ["PROJ_LIB"] = "/g/data/v45/jm5970/env/track_env/share/proj"
import xarray as xr
import cmocean as cm
from trackeddy.tracking import *
from trackeddy.datastruct import *
from trackeddy.geometryfunc import *
from trackeddy.physics import *
from trackeddy.plotfunc import *
from numpy import *
from calendar import monthrange
import numpy.ma as ma
import datetime

from os import listdir
from os.path import isfile, join

year=sys.argv[1]
outputfilenumber=sys.argv[1]
index_files=int(sys.argv[2])
divisions=int(sys.argv[3])

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
lon=data.longitude.values
lat=data.latitude.values

init_time=datetime.datetime.strptime(str(data.time.isel(time=0).values).split('T')[0], "%Y-%m-%d")
print(init_time)

outfolder='/g/data/v45/jm5970/trackeddy_output/AVISO+/'

sshatime=data.sla.values        
sshatime=ma.masked_where(sshatime <= -2147483647, sshatime)

print('End loading data')
sshashape=np.shape(sshatime)

# Output data path
#try:
analysedatap=np.load('{0}npy/aviso_{1}-{2:03}_pos.npy'.format(outfolder,year,index_files),allow_pickle=True)
dictanalysep=analysedatap.item()
reconstruct_p=reconstruct_syntetic(sshashape,lon,lat,dictanalysep)
reconstruct_p=ma.array(reconstruct_p,mask=sshatime.mask)
filename='{0}post-processing/satellite_reconstructed_field_{1}_{2:03}_cyc.nc'.format(outfolder,outputfilenumber,index_files)
vargeonc(filename,lat,lon,reconstruct_p,shape(reconstruct_p)[0],'SSHa_cyc',init_time,nc_description='Cyclonic reconstructed Field from SSHa field using Trackeddy.',units='m',dt='',dim='2D')
#except:
#   pass

#try:
analysedatan=np.load('{0}npy/aviso_{1}-{2:03}_neg.npy'.format(outfolder,year,index_files),allow_pickle=True)
dictanalysen=analysedatan.item()
reconstruct_n=-reconstruct_syntetic(sshashape,lon,lat,dictanalysen)
reconstruct_n=ma.array(reconstruct_n,mask=sshatime.mask)
filename='{0}post-processing/satellite_reconstructed_field_{1}_{2:03}_acyc.nc'.format(outfolder,outputfilenumber,index_files)
vargeonc(filename,lat,lon,reconstruct_n,shape(reconstruct_n)[0],'SSHa_acyc',init_time,nc_description='Anticyclonic reconstructed Field from SSHa field using Trackeddy.',units='m',dt='',dim='2D')
#except:
#   pass

#try:
reconstruct=reconstruct_p+reconstruct_n

plt.pcolormesh(lon,lat,reconstruct[0,:,:])
plt.savefig(outfolder+'post-processing/satellite_reconstructed_field_'+outputfilenumber+'.png')

filename='{0}post-processing/satellite_reconstructed_field_{1}_{2:03}.nc'.format(outfolder,outputfilenumber,index_files)
vargeonc(filename,lat,lon,reconstruct,shape(reconstruct)[0],'SSHa_reconstruct',init_time,nc_description='Reconstructed Field from SSHa field using Trackeddy.',units='m',dt='',dim='2D')

filename='{0}post-processing/satellite_reconstructed_field_{1}_{2:03}_diff.nc'.format(outfolder,outputfilenumber,index_files)
vargeonc(filename,lat,lon,sshatime-reconstruct,shape(reconstruct)[0],'SSHa_reconstruct',init_time,nc_description='Reconstructed Field from SSHa field using Trackeddy.',units='m',dt='',dim='2D')
#except:
#   pass
