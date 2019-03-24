import time
tic=time.time()
import matplotlib
matplotlib.use('Agg')
import trackeddy.tracking as ttrack
from trackeddy.savedata import *
from trackeddy.geometryfunc import *
from trackeddy.physics import *
from pylab import *
import random
import pdb
import cmocean as cm

import matplotlib.gridspec as gridspec

import trackeddy.utils.field_generator as fg

init_time=int(sys.argv[1])

outfolder='/g/data/v45/jm5970/trackeddy_output/validation/'
t  = 10

x = linspace(0,360,3600)
y = linspace(-90,90,3600)

# print("Generate field")
# gf=fg.Generate_field(0.7,0.7,n,xx,yy,'Nint')
# data = gf.assemble_field(t,margin=0)

data = zeros((t,3600,3600))
for tt in range(t):
    nn=randint(700, 1000)
    print("t ="+str(tt)+" n ="+str(nn))
    gf=fg.Generate_field(0.5,0.5,nn,x,y,'Nint')
    data[tt,:,:] = gf.assemble_field(1,margin=0)


filename=outfolder+'output/validation_field_'+str(init_time)+'.nc'
vargeonc(filename,y,x,data,shape(data)[0],'ssha',init_time*t,nc_description='Trackeddy Validation Field.',units='m',dt='',dim='2D')

################################################################################
################################################################################
#################################### FLAT ######################################
################################################################################
################################################################################

preferences={'ellipse':0.85,'eccentricity':0.85,'gaussian':0.8}
eddytd={}
eddytdn={}

t0 = 0
t  = 1

levels = {'max':data.max(),'min':0.05,'step':0.05}
eddytd = ttrack.analyseddyzt(data,x,y,t0,t,1,levels,\
    preferences=preferences,areamap='',mask='',maskopt='forcefit',\
    destdir='',physics='',diagnostics=False,plotdata=False,pprint=True,\
    debug=False)

####

levels  = {'max':data.min(),'min':-0.05,'step':-0.05}
eddytdn = ttrack.analyseddyzt(data,x,y,t0,t,1,levels,\
    preferences=preferences,areamap='',mask='',maskopt='forcefit',\
    destdir='',physics='',diagnostics=False,plotdata=False,pprint=True,\
    debug=False)

pos_f = reconstruct_syntetic(shape(data),x,y,eddytd)
neg_f = reconstruct_syntetic(shape(data),x,y,eddytdn)

f_field = pos_f+neg_f

filename=outfolder+'output/validation_field_reconstruct_'+str(init_time)+'.nc'
vargeonc(filename,y,x,f_field,shape(f_field)[0],'ssh',init_time*t,nc_description='Trackeddy Validation Field.',units='m',dt='',dim='2D')

################################################################################
#################################### WAVE ######################################
################################################################################
################################################################################

amplitude = 1
frequency = 20
phase = 1
waves = zeros(shape(data))

X,Y = meshgrid(x,y)
for t in range(0,t):
    r = X+y/10
    waves[t,:,:] = 0.3*sin(r*frequency-t + phase)

wave_data = waves+data

levels = {'max':wave_data.max(),'min':0.05,'step':0.05}
eddytd=ttrack.analyseddyzt(wave_data,x,y,0,t,1,levels,preferences=preferences,areamap='',mask='',maskopt='forcefit'\
                    ,destdir='',physics='',diagnostics=False,plotdata=False,pprint=True)

levels = {'max':wave_data.min(),'min':-0.05,'step':-0.05}
eddytdn=ttrack.analyseddyzt(wave_data,x,y,0,t,1,levels,preferences=preferences,areamap='',mask='',maskopt='forcefit'\
                    ,destdir='',physics='',diagnostics=False,plotdata=False,pprint=True)

pos_w = reconstruct_syntetic(shape(wave_data),x,y,eddytd)
neg_w = reconstruct_syntetic(shape(wave_data),x,y,eddytdn)

w_field = pos_w+neg_w

filename=outfolder+'output/validation_field_wave_'+str(init_time)+'.nc'
vargeonc(filename,y,x,w_field,shape(w_field)[0],'ssh',init_time*t,nc_description='Trackeddy Validation Field.',units='m',dt='',dim='2D')

################################################################################
################################################################################
#################################### JETS ######################################
################################################################################
################################################################################

k_y = 3
phase = 1
k_x = 2
jets = zeros(shape(data))
for t in range(0,t):
    r = Y
    k_y=random.uniform(2, 3)
    phase=random.uniform(0, 1)
    k_x=random.uniform(1, 2)
    amp=0.3
    jets[t,:,:] = amp*cos((k_y*(k_y*Y+phase+sin(k_x*X-t))))
jet_data = jets+data

levels = {'max':jet_data.max(),'min':0.05,'step':0.05}
eddytd=ttrack.analyseddyzt(jet_data,x,y,0,t,1,levels,preferences=preferences,areamap='',mask='',maskopt='forcefit'\
                    ,destdir='',physics='',diagnostics=False,plotdata=False,pprint=True)

levels = {'max':jet_data.min(),'min':-0.05,'step':-0.05}
eddytdn=ttrack.analyseddyzt(jet_data,x,y,0,t,1,levels,preferences=preferences,areamap='',mask='',maskopt='forcefit'\
                    ,destdir='',physics='',diagnostics=False,plotdata=False,pprint=True)

pos_f = reconstruct_syntetic(shape(jet_data),x,y,eddytd)
neg_f = reconstruct_syntetic(shape(jet_data),x,y,eddytdn)

j_field = pos_f+neg_f

filename=outfolder+'output/validation_field_jet_'+str(init_time)+'.nc'
vargeonc(filename,y,x,j_field,shape(j_field)[0],'ssh',init_time*t,nc_description='Trackeddy Validation Field.',units='m',dt='',dim='2D')

################################################################################
################################################################################
##################################### KE #######################################
################################################################################
################################################################################

m_ke_c = []
m_ke_f = []
m_ke_w = []
m_ke_j = []

for tt in range(shape(data)[0]):
    u_c,v_c = geovelfield( data[tt,:,:]  ,x,y)
    u_f,v_f = geovelfield(f_field[tt,:,:],x,y)
    u_w,v_w = geovelfield(w_field[tt,:,:],x,y)
    u_j,v_j = geovelfield(j_field[tt,:,:],x,y)
    ke_c = KE(u_c,v_c)
    ke_f = KE(u_f,v_f)
    ke_w = KE(u_w,v_w)
    ke_j = KE(u_j,v_j)
    m_ke_c.append(mean(ke_c))
    m_ke_f.append(mean(ke_f))
    m_ke_w.append(mean(ke_w))
    m_ke_j.append(mean(ke_j))


filename=outfolder+'output/u_c'+str(init_time)+'.nc'
vargeonc(filename,y,x,u_c,shape(j_field)[0],'u',init_time*t,nc_description='Trackeddy Validation Field velocity.',units='m/s',dt='',dim='2D')
filename=outfolder+'output/v_c'+str(init_time)+'.nc'
vargeonc(filename,y,x,v_c,shape(j_field)[0],'v',init_time*t,nc_description='Trackeddy Validation Field velocity.',units='m/s',dt='',dim='2D')


filename=outfolder+'output/u_f'+str(init_time)+'.nc'
vargeonc(filename,y,x,u_f,shape(j_field)[0],'u',init_time*t,nc_description='Trackeddy Validation Field velocity.',units='m/s',dt='',dim='2D')
filename=outfolder+'output/v_f'+str(init_time)+'.nc'
vargeonc(filename,y,x,v_f,shape(j_field)[0],'v',init_time*t,nc_description='Trackeddy Validation Field velocity.',units='m/s',dt='',dim='2D')


filename=outfolder+'output/u_w'+str(init_time)+'.nc'
vargeonc(filename,y,x,u_w,shape(j_field)[0],'u',init_time*t,nc_description='Trackeddy Validation Field velocity.',units='m/s',dt='',dim='2D')
filename=outfolder+'output/v_w'+str(init_time)+'.nc'
vargeonc(filename,y,x,v_w,shape(j_field)[0],'v',init_time*t,nc_description='Trackeddy Validation Field velocity.',units='m/s',dt='',dim='2D')


filename=outfolder+'output/u_j'+str(init_time)+'.nc'
vargeonc(filename,y,x,u_j,shape(j_field)[0],'u',init_time*t,nc_description='Trackeddy Validation Field velocity.',units='m/s',dt='',dim='2D')
filename=outfolder+'output/v_j'+str(init_time)+'.nc'
vargeonc(filename,y,x,v_j,shape(j_field)[0],'v',init_time*t,nc_description='Trackeddy Validation Field velocity.',units='m/s',dt='',dim='2D')


filename=outfolder+'output/ke_c'+str(init_time)+'.nc'
vargeonc(filename,y,x,ke_c,shape(j_field)[0],'teke',init_time*t,nc_description='Trackeddy Validation Field velocity.',units='m2/s2',dt='',dim='2D')
filename=outfolder+'output/ke_f'+str(init_time)+'.nc'
vargeonc(filename,y,x,ke_f,shape(j_field)[0],'teke',init_time*t,nc_description='Trackeddy Validation Field velocity.',units='m2/s2',dt='',dim='2D')
filename=outfolder+'output/ke_w'+str(init_time)+'.nc'
vargeonc(filename,y,x,ke_w,shape(j_field)[0],'teke',init_time*t,nc_description='Trackeddy Validation Field velocity.',units='m2/s2',dt='',dim='2D')
filename=outfolder+'output/Ke_j'+str(init_time)+'.nc'
vargeonc(filename,y,x,ke_j,shape(j_field)[0],'teke',init_time*t,nc_description='Trackeddy Validation Field velocity.',units='m2/s2',dt='',dim='2D')

################################################################################
################################################################################
#################################### PLOT ######################################
################################################################################
################################################################################

stats={'control':m_ke_c,'flat':m_ke_f,'wave':m_ke_w,'jet':m_ke_j}

save(outfile+'stats_'+str(init_time)+'.npy',stats)
toc=time.time()

print("######## ELAPSED TIME: ###########")
print("######## %2f s ###########" % (toc-tic))

