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

init_time = datetime.strptime(str(time[time_division[division_number][0]]), "%Y-%m-%d %H:%M:%S")

print(init_time)

#eta=ncfile.sea_level.values[time_division[division_number][0]:time_division[division_number][-1]+1,:,:]
#etashape=shape(eta)

# Output data patha
filepath = outfolder+'npy/ACCESS_01_{0:05}_{1:02}_pos.npy'.format(outputfilenumber,division_number) 
analysedatap=np.load(filepath,allow_pickle=True)
dictanalysep=analysedatap.item()

pos_pd = dict2pd(dictanalysep,inittime=init_time.strftime("%d-%m-%Y"),n=0,polarity='pos',ensemble=None)

filepath = outfolder+'npy/ACCESS_01_{0:05}_{1:02}_neg.npy'.format(outputfilenumber,division_number) 
analysedatan=np.load(filepath,allow_pickle=True)
dictanalysen=analysedatan.item()

neg_pd = dict2pd(dictanalysen,inittime=init_time.strftime("%d-%m-%Y"),n=0,polarity='neg',ensemble=None)

pd_result = pd.concat([pos_pd,neg_pd])
pd_result.to_csv(outfolder+'pandas/csv_identified_eddies_{0:05}_{1:02}.csv'.format(outputfilenumber,division_number))
