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
from trackeddy.init import *
from trackeddy.physics import *
from trackeddy.plotfunc import *
from numpy import *
from calendar import monthrange

year=sys.argv[1]
monthsin=int(sys.argv[2])
monthsend=int(sys.argv[3])

print('Analizing the year ',year,'in the months[',monthsin,'-',monthsend,']')
inputfiles='/g/data/ua8/CMEMS_SeaLevel/v4-0/'+year+'/'

outputfilenumber=sys.argv[1]
outfolder='/g/data/v45/jm5970/trackeddy_out/'

datashapetime=0
for month in range(monthsin,monthsend):
    datashapetime=datashapetime+monthrange(int(year), month)[1]

# Import SSH values to python environment.
ncfile=Dataset(inputfiles+'dt_global_allsat_phy_l4_'+year+'0101_20180115.nc')
ssha=np.squeeze(ncfile.variables['sla'][:])
# Import geographic coordinates (Lon,Lat)
lon=ncfile.variables['longitude'][:]
lat=ncfile.variables['latitude'][:]

sshatime=zeros([datashapetime,shape(ssha)[0],shape(ssha)[1]])
ii=0
print('Start loading data')
for month in range(monthsin,monthsend):
    daysmonth=monthrange(int(year), month)[1]
    for days in range(1,daysmonth+1):
        ncfile=Dataset(inputfiles+'dt_global_allsat_phy_l4_'+year+'%02d'%month+'%02d'%days+'_20180115.nc')
        #ncfile=Dataset(inputfiles+'dt_global_allsat_phy_l4_'+year+'%02d'%month+'%02d'%days+'_20170110.nc')
        sshatime[ii,:,:]=squeeze(ncfile.variables['sla'][:])
        ii=ii+1
        ncfile.close()

sshatime=ma.masked_where(sshatime <= -2147483647, sshatime)
print('End loading data')
sshashape=np.shape(sshatime)
# Output data path
try:
   analysedatap=np.load(outfolder+year+str(monthsin)+'-'+str(monthsend)+'_pos_satellite.npy')
   dictanalysep=analysedatap.item()
   reconstruct_p=reconstruct_syntetic(sshashape,lon,lat,dictanalysep)
   
   filename=outfolder+'output/satellite_reconstructed_field_'+outputfilenumber+'_'+str(monthsin)+'_'+str(monthsend)+'_cyc.nc'
   vargeonc(filename,lat,lon,reconstruct_p,shape(reconstruct_p)[0],'SSHa_cyc',nc_description='Cyclonic reconstructed Field from SSHa field using Trackeddy.',units='m',dt='',dim='2D')
except:
   pass

try:
   analysedatan=np.load(outfolder+year+str(monthsin)+'-'+str(monthsend)+'_neg_satellite.npy')
   dictanalysen=analysedatan.item()
   reconstruct_n=reconstruct_syntetic(sshashape,lon,lat,dictanalysen)

   filename=outfolder+'output/satellite_reconstructed_field_'+outputfilenumber+'_'+str(monthsin)+'_'+str(monthsend)+'_acyc.nc'
   vargeonc(filename,lat,lon,reconstruct_n,shape(reconstruct_n)[0],'SSHa_acyc',nc_description='Anticyclonic reconstructed Field from SSHa field using Trackeddy.',units='m',dt='',dim='2D')
except:
   pass

try:
   reconstruct=reconstruct_p+reconstruct_n

   plt.pcolormesh(lon,lat,reconstruct[0,:,:])
   plt.savefig(outfolder+'output/satellite_reconstructed_field_'+outputfilenumber+'.png')

   filename=outfolder+'output/satellite_reconstructed_field_'+outputfilenumber+'_'+str(monthsin)+'_'+str(monthsend)+'.nc'
   vargeonc(filename,lat,lon,reconstruct,shape(reconstruct)[0],'SSHa_reconstruct',nc_description='Reconstructed Field from SSHa field using Trackeddy.',units='m',dt='',dim='2D')

   filename=outfolder+'output/satellite_reconstructed_field_'+outputfilenumber+'_'+str(monthsin)+'_'+str(monthsend)+'_diff.nc'
   vargeonc(filename,lat,lon,sshatime-reconstruct,shape(reconstruct)[0],'SSHa_reconstruct',nc_description='Reconstructed Field from SSHa field using Trackeddy.',units='m',dt='',dim='2D')
except:
   pass
