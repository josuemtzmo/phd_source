import sys
import numpy as np
import netCDF4 as nc4
from datetime import date

j0=int(sys.argv[1])
j1=int(sys.argv[2])
i0=int(sys.argv[3])
i1=int(sys.argv[4])

inputfile=sys.argv[5]
outputfile=sys.argv[6]

topogfullNC=nc4.Dataset(inputfile)
globaldepth=topogfullNC.variables['depth']

regiondepth=globaldepth[j0:j1,i0:i1] 

f = nc4.Dataset(outputfile,'w', format='NETCDF4')
ny=f.createDimension('ny', np.shape(regiondepth)[0])
nx=f.createDimension('nx', np.shape(regiondepth)[1])
ntiles=f.createDimension('ntiles', 1)

ny = range(0,np.shape(regiondepth)[0])
nx = range(0,np.shape(regiondepth)[1])
ntiles = 1

depth = f.createVariable('depth', 'f4',('ny', 'nx'))
depth[:,:] = regiondepth
today = date.today()
f.history = today.strftime("%d/%m/%y") + "python topography_subregion.py " + str(j0) + str(j1) + str(i0) + str(i1)+ inputfile +" "+ outputfile 
f.close()
