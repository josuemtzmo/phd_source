from calendar import monthrange
from netCDF4 import Dataset
import numpy as np
from trackeddy.physics import *
import datetime
import pylab as plt
from matplotlib import gridspec
import cmocean as cm
from mpl_toolkits.basemap import Basemap



def sat_seasonal_variation(year,monthsin,monthsend,areamap='',plot=True,hemisphere='',days=''):
    index=0
    if days=='':
        days=365
        
    eke_mean=np.zeros(days)
    
    for ii in range(len(monthsin)):
        #print('File:',monthsin[ii])
        ufilename=Dataset('/home/156/jm5970/notebooks/traceddy/data.input/ssha_u_satellite_'+str(year)+'_'+str(monthsin[ii])+'yrs.nc')
        lon=ufilename.variables['Longitude'][:]
        lat=ufilename.variables['Latitude'][:]
        #print(len(lon),len(lat))
        if areamap=='':
            areamap=np.array([[0,len(lon)],[0,len(lat)]])
        lon=lon[areamap[0,0]:areamap[0,1]]
        lat=lat[areamap[1,0]:areamap[1,1]]
        u_prime=np.squeeze(ufilename.variables['U'][:,areamap[1,0]:areamap[1,1],areamap[0,0]:areamap[0,1]])
        #print(np.shape(u_prime))
        #print(areamap[0,0],areamap[0,1],areamap[1,0],areamap[1,1])
        #print(ufilename)
        vfilename=Dataset('/home/156/jm5970/notebooks/traceddy/data.input/ssha_v_satellite_'+str(year)+'_'+str(monthsin[ii])+'yrs.nc')
        v_prime=np.squeeze(vfilename.variables['V'][:,areamap[1,0]:areamap[1,1],areamap[0,0]:areamap[0,1]])
        dayssum=0
    
        for month in range(monthsin[ii],monthsend[ii]):
            dayssum=dayssum+monthrange(int(year), month)[1] 

        for tt in range(0,np.shape(v_prime)[0]):
            ekecal=KE(u_prime[tt,:,:],v_prime[tt,:,:])
            eke_mean[index]=np.nanmean(ekecal)
            index=index+1
    if plot==True:        
    
        numdays=len(eke_mean)
        base = datetime.datetime(year, 1, 1, 0, 0)
        date_list = [base + datetime.timedelta(days=x) for x in range(0, numdays)]

        fig, ax = plt.subplots(1,2,figsize=(18,3),gridspec_kw = {'width_ratios':[3, 2]})
        #gs = gridspec.GridSpec(1,2, width_ratios=[3, 1]) 
        ax[0].plot(date_list,eke_mean,'-')
        if hemisphere=='North':
            ax[0].text(date_list[20], max(eke_mean)-np.mean(eke_mean)/4,'Winter',color='blue')
            ax[0].fill_between(date_list[0:60], eke_mean.min(), eke_mean.max(), facecolor='cyan', alpha=0.1)
            ax[0].text(date_list[95], max(eke_mean)-np.mean(eke_mean)/4,'Spring',color='black')
            ax[0].fill_between(date_list[60:150], eke_mean.min(), eke_mean.max(), facecolor='yellow', alpha=0.1)
            ax[0].text(date_list[185], max(eke_mean)-np.mean(eke_mean)/4,'Summer',color='red')
            ax[0].fill_between(date_list[150:240], eke_mean.min(), eke_mean.max(), facecolor='red', alpha=0.1)
            ax[0].text(date_list[280], max(eke_mean)-np.mean(eke_mean)/4,'Autumn',color='m')
            ax[0].fill_between(date_list[240:330], eke_mean.min(), eke_mean.max(), facecolor='orange', alpha=0.1)
            ax[0].fill_between(date_list[330:], eke_mean.min(), eke_mean.max(), facecolor='cyan', alpha=0.1)
        else:
            ax[0].text(date_list[20], max(eke_mean)-np.mean(eke_mean)/4,'Summer',color='red')
            ax[0].fill_between(date_list[0:60], eke_mean.min(), eke_mean.max(), facecolor='red', alpha=0.1)
            ax[0].text(date_list[95], max(eke_mean)-np.mean(eke_mean)/4,'Autumn',color='m')
            ax[0].fill_between(date_list[60:150], eke_mean.min(), eke_mean.max(), facecolor='orange', alpha=0.1)
            ax[0].text(date_list[185], max(eke_mean)-np.mean(eke_mean)/4,'Winter',color='Blue')
            ax[0].fill_between(date_list[150:240], eke_mean.min(), eke_mean.max(), facecolor='cyan', alpha=0.1)
            ax[0].text(date_list[280], max(eke_mean)-np.mean(eke_mean)/4,'Spring',color='Black')
            ax[0].fill_between(date_list[240:330], eke_mean.min(), eke_mean.max(), facecolor='yellow', alpha=0.1)
            ax[0].fill_between(date_list[330:], eke_mean.min(), eke_mean.max(), facecolor='red', alpha=0.1)
            
        ax[0].grid(True)
        ax[0].set_xlim(date_list[0],date_list[-1])
        ax[0].set_ylim(eke_mean.min(), eke_mean.max())

        monthsFmt = plt.DateFormatter("%b")
        ax[0].xaxis.set_major_formatter(monthsFmt)
        
        map = Basemap(projection='mbtfpq',lon_0=-180,resolution='c',ax=ax[1])
        lonmm,latmm=np.meshgrid(lon,lat)
        lonm,latm=map(lonmm,latmm)
        map.drawmeridians(np.arange(0,360,90),labels=[0,0,0,1],fontsize=10)
        map.drawparallels(np.arange(-90,90,30),labels=[1,1,0,0],fontsize=10)
        map.fillcontinents(color='black',lake_color='aqua')
        map.drawcoastlines()
        map.drawcoastlines()
        im=ax[1].pcolormesh(lonm,latm,ekecal,cmap=cm.cm.amp,vmin=0,vmax=np.mean(eke_mean))
        fig.colorbar(im, orientation='vertical')
    return eke_mean

def sim_seasonal_variation(fileinit,fileend,areamap='',plot=True,hemisphere='',days=''):
    index=0
    if days=='':
        days=365
    eke_mean=np.zeros(days)
    for ii in range(fileinit,fileend):
        ufilename=Dataset('/home/156/jm5970/notebooks/traceddy/data.input/ssha_'+str(ii)+'_u_1yrs.nc')
        lon=ufilename.variables['Longitude'][:]
        lat=ufilename.variables['Latitude'][:]
        #print(len(lon),len(lat))
        if areamap=='':
            areamap=np.array([[0,len(lon)],[0,len(lat)]])
        lon=lon[areamap[0,0]:areamap[0,1]]
        lat=lat[areamap[1,0]:areamap[1,1]]
        
        u_prime=np.squeeze(ufilename.variables['U'][:,areamap[1,0]:areamap[1,1],areamap[0,0]:areamap[0,1]])
        vfilename=Dataset('/home/156/jm5970/notebooks/traceddy/data.input/ssha_'+str(ii)+'_v_1yrs.nc')
        v_prime=np.squeeze(vfilename.variables['V'][:,areamap[1,0]:areamap[1,1],areamap[0,0]:areamap[0,1]])

        eke=np.zeros([np.shape(v_prime)[0],np.shape(v_prime)[1],np.shape(v_prime)[2]])
        for tt in range(0,np.shape(v_prime)[0]):
            eke_c=np.array(KE(u_prime[tt,:,:],v_prime[tt,:,:]))
            eke_mean[index]=np.nanmean(eke_c)
            index=index+1
    if plot==True:        
    
        numdays=len(eke_mean)
        base = datetime.datetime(1992, 1, 1, 0, 0)
        date_list = [base + datetime.timedelta(days=x) for x in range(0, numdays)]

        fig, ax = plt.subplots(1,2,figsize=(18,3),gridspec_kw = {'width_ratios':[4, 1]})
        #gs = gridspec.GridSpec(1,2, width_ratios=[3, 1]) 
        ax[0].plot(date_list,eke_mean,'-')
        if hemisphere=='North':
            ax[0].text(date_list[20], max(eke_mean)-np.mean(eke_mean)/4,'Winter',color='blue')
            ax[0].fill_between(date_list[0:60], eke_mean.min(), eke_mean.max(), facecolor='cyan', alpha=0.1)
            ax[0].text(date_list[95], max(eke_mean)-np.mean(eke_mean)/4,'Spring',color='black')
            ax[0].fill_between(date_list[60:150], eke_mean.min(), eke_mean.max(), facecolor='yellow', alpha=0.1)
            ax[0].text(date_list[185], max(eke_mean)-np.mean(eke_mean)/4,'Summer',color='red')
            ax[0].fill_between(date_list[150:240], eke_mean.min(), eke_mean.max(), facecolor='red', alpha=0.1)
            ax[0].text(date_list[280], max(eke_mean)-np.mean(eke_mean)/4,'Autumn',color='m')
            ax[0].fill_between(date_list[240:330], eke_mean.min(), eke_mean.max(), facecolor='orange', alpha=0.1)
            ax[0].fill_between(date_list[330:], eke_mean.min(), eke_mean.max(), facecolor='cyan', alpha=0.1)
        else:
            ax[0].text(date_list[20], max(eke_mean)-np.mean(eke_mean)/4,'Summer',color='red')
            ax[0].fill_between(date_list[0:60], eke_mean.min(), eke_mean.max(), facecolor='red', alpha=0.1)
            ax[0].text(date_list[95], max(eke_mean)-np.mean(eke_mean)/4,'Autumn',color='m')
            ax[0].fill_between(date_list[60:150], eke_mean.min(), eke_mean.max(), facecolor='orange', alpha=0.1)
            ax[0].text(date_list[185], max(eke_mean)-np.mean(eke_mean)/4,'Winter',color='Blue')
            ax[0].fill_between(date_list[150:240], eke_mean.min(), eke_mean.max(), facecolor='cyan', alpha=0.1)
            ax[0].text(date_list[280], max(eke_mean)-np.mean(eke_mean)/4,'Spring',color='Black')
            ax[0].fill_between(date_list[240:330], eke_mean.min(), eke_mean.max(), facecolor='yellow', alpha=0.1)
            ax[0].fill_between(date_list[330:], eke_mean.min(), eke_mean.max(), facecolor='red', alpha=0.1)
            
        ax[0].grid(True)
        ax[0].set_xlim(date_list[0],date_list[-1])
        ax[0].set_ylim(eke_mean.min(), eke_mean.max())

        monthsFmt = plt.DateFormatter("%b")
        ax[0].xaxis.set_major_formatter(monthsFmt)
        
        map = Basemap(projection='ortho',lat_0=-90,lon_0=-100,resolution='c',ax=ax[1])
        lonmm,latmm=np.meshgrid(lon,lat)
        lonm,latm=map(lonmm,latmm)
        map.drawmeridians(np.arange(0,360,90),labels=[0,0,0,1],fontsize=10)
        map.drawparallels(np.arange(-90,90,30),labels=[1,1,0,0],fontsize=10)
        map.fillcontinents(color='black',lake_color='aqua')
        map.drawcoastlines()
        map.drawcoastlines()
        im=ax[1].pcolormesh(lonm,latm,eke_c,cmap=cm.cm.amp,vmin=0,vmax=eke_mean.max())
        fig.colorbar(im, orientation='vertical')
    return eke_mean



def sim_seasonal_variation_eke(fileinit,fileend,areamap='',plot=True,hemisphere='',days=''):
    index=0
    if days=='':
        days=365
    eke_mean=np.zeros(days)
    for ii in range(fileinit,fileend):
        ufilename=Dataset('/home/156/jm5970/notebooks/traceddy/data.input/'+str(ii)+'_u_prime_eddy_1yrs.nc')
        lon=ufilename.variables['Longitude'][:]
        lat=ufilename.variables['Latitude'][:]
        #print(len(lon),len(lat))
        if areamap=='':
            areamap=np.array([[0,len(lon)],[0,len(lat)]])
        lon=lon[areamap[0,0]:areamap[0,1]]
        lat=lat[areamap[1,0]:areamap[1,1]]
        
        u_prime=np.squeeze(ufilename.variables['U'][:,areamap[1,0]:areamap[1,1],areamap[0,0]:areamap[0,1]])
        vfilename=Dataset('/home/156/jm5970/notebooks/traceddy/data.input/'+str(ii)+'_v_prime_eddy_1yrs.nc')
        v_prime=np.squeeze(vfilename.variables['V'][:,areamap[1,0]:areamap[1,1],areamap[0,0]:areamap[0,1]])

        eke=np.zeros([np.shape(v_prime)[0],np.shape(v_prime)[1],np.shape(v_prime)[2]])
        for tt in range(0,np.shape(v_prime)[0]):
            eke_c=np.array(KE(u_prime[tt,:,:],v_prime[tt,:,:]))
            eke_mean[index]=np.nanmean(eke_c)
            index=index+1
    if plot==True:        
    
        numdays=len(eke_mean)
        base = datetime.datetime(1992, 1, 1, 0, 0)
        date_list = [base + datetime.timedelta(days=x) for x in range(0, numdays)]

        fig, ax = plt.subplots(1,2,figsize=(18,3),gridspec_kw = {'width_ratios':[4, 1]})
        #gs = gridspec.GridSpec(1,2, width_ratios=[3, 1]) 
        ax[0].plot(date_list,eke_mean,'-')
        if hemisphere=='North':
            ax[0].text(date_list[20], max(eke_mean)-np.mean(eke_mean)/4,'Winter',color='blue')
            ax[0].fill_between(date_list[0:60], eke_mean.min(), eke_mean.max(), facecolor='cyan', alpha=0.1)
            ax[0].text(date_list[95], max(eke_mean)-np.mean(eke_mean)/4,'Spring',color='black')
            ax[0].fill_between(date_list[60:150], eke_mean.min(), eke_mean.max(), facecolor='yellow', alpha=0.1)
            ax[0].text(date_list[185], max(eke_mean)-np.mean(eke_mean)/4,'Summer',color='red')
            ax[0].fill_between(date_list[150:240], eke_mean.min(), eke_mean.max(), facecolor='red', alpha=0.1)
            ax[0].text(date_list[280], max(eke_mean)-np.mean(eke_mean)/4,'Autumn',color='m')
            ax[0].fill_between(date_list[240:330], eke_mean.min(), eke_mean.max(), facecolor='orange', alpha=0.1)
            ax[0].fill_between(date_list[330:], eke_mean.min(), eke_mean.max(), facecolor='cyan', alpha=0.1)
        else:
            ax[0].text(date_list[20], max(eke_mean)-np.mean(eke_mean)/4,'Summer',color='red')
            ax[0].fill_between(date_list[0:60], eke_mean.min(), eke_mean.max(), facecolor='red', alpha=0.1)
            ax[0].text(date_list[95], max(eke_mean)-np.mean(eke_mean)/4,'Autumn',color='m')
            ax[0].fill_between(date_list[60:150], eke_mean.min(), eke_mean.max(), facecolor='orange', alpha=0.1)
            ax[0].text(date_list[185], max(eke_mean)-np.mean(eke_mean)/4,'Winter',color='Blue')
            ax[0].fill_between(date_list[150:240], eke_mean.min(), eke_mean.max(), facecolor='cyan', alpha=0.1)
            ax[0].text(date_list[280], max(eke_mean)-np.mean(eke_mean)/4,'Spring',color='Black')
            ax[0].fill_between(date_list[240:330], eke_mean.min(), eke_mean.max(), facecolor='yellow', alpha=0.1)
            ax[0].fill_between(date_list[330:], eke_mean.min(), eke_mean.max(), facecolor='red', alpha=0.1)
            
        ax[0].grid(True)
        ax[0].set_xlim(date_list[0],date_list[-1])
        ax[0].set_ylim(eke_mean.min(), eke_mean.max())

        monthsFmt = plt.DateFormatter("%b")
        ax[0].xaxis.set_major_formatter(monthsFmt)
        
        map = Basemap(projection='ortho',lat_0=-90,lon_0=-100,resolution='c',ax=ax[1])
        lonmm,latmm=np.meshgrid(lon,lat)
        lonm,latm=map(lonmm,latmm)
        map.drawmeridians(np.arange(0,360,90),labels=[0,0,0,1],fontsize=10)
        map.drawparallels(np.arange(-90,90,30),labels=[1,1,0,0],fontsize=10)
        map.fillcontinents(color='black',lake_color='aqua')
        map.drawcoastlines()
        map.drawcoastlines()
        im=ax[1].pcolormesh(lonm,latm,eke_c,cmap=cm.cm.amp,vmin=0,vmax=eke_mean.max())
        fig.colorbar(im, orientation='vertical')
    return eke_mean

def sim_EKE_eddy_seasonal_variation(fileinit,fileend,areamap='',plot=True,hemisphere='',basemap=True,days=''):
    index=0
    if days=='':
        days=365
    eke_mean=np.zeros(days)
    for ii in range(fileinit,fileend):
        ekefile=Dataset('/home/156/jm5970/notebooks/traceddy/data.input/eke_eddy_'+str(ii)+'.nc')
        lon=ekefile.variables['Longitude'][:]
        lat=ekefile.variables['Latitude'][:]
        #print(len(lon),len(lat))
        if areamap=='':
            areamap=np.array([[0,len(lon)],[0,len(lat)]])
        lon=lon[areamap[0,0]:areamap[0,1]]
        lat=lat[areamap[1,0]:areamap[1,1]]
        
        eke=np.squeeze(ekefile.variables['EKE_eddy'])
        for tt in range(0,np.shape(eke)[0]):
            eket=eke[tt,:,:]
            eket[eket==0]=np.nan
            eke_mean[index]=np.nanmean(eket[:,:])
            index=index+1
    if plot==True:        
    
        numdays=len(eke_mean)
        base = datetime.datetime(1992, 1, 1, 0, 0)
        date_list = [base + datetime.timedelta(days=x) for x in range(0, numdays)]
        if basemap==True:
            fig, ax = plt.subplots(1,2,figsize=(18,3),gridspec_kw = {'width_ratios':[4, 1]})
        else:
            fig, ax = plt.subplots(1,1,figsize=(18,3))
            ax=[ax]
        #gs = gridspec.GridSpec(1,2, width_ratios=[3, 1]) 
        ax[0].plot(date_list,eke_mean,'-')
        if hemisphere=='North':
            ax[0].text(date_list[20], max(eke_mean)-np.mean(eke_mean)/4,'Winter',color='blue')
            ax[0].fill_between(date_list[0:60], eke_mean.min(), eke_mean.max(), facecolor='cyan', alpha=0.1)
            ax[0].text(date_list[95], max(eke_mean)-np.mean(eke_mean)/4,'Spring',color='black')
            ax[0].fill_between(date_list[60:150], eke_mean.min(), eke_mean.max(), facecolor='yellow', alpha=0.1)
            ax[0].text(date_list[185], max(eke_mean)-np.mean(eke_mean)/4,'Summer',color='red')
            ax[0].fill_between(date_list[150:240], eke_mean.min(), eke_mean.max(), facecolor='red', alpha=0.1)
            ax[0].text(date_list[280], max(eke_mean)-np.mean(eke_mean)/4,'Autumn',color='m')
            ax[0].fill_between(date_list[240:330], eke_mean.min(), eke_mean.max(), facecolor='orange', alpha=0.1)
            ax[0].fill_between(date_list[330:], eke_mean.min(), eke_mean.max(), facecolor='cyan', alpha=0.1)
        else:
            ax[0].text(date_list[20], max(eke_mean)-np.mean(eke_mean)/4,'Summer',color='red')
            ax[0].fill_between(date_list[0:60], eke_mean.min(), eke_mean.max(), facecolor='red', alpha=0.1)
            ax[0].text(date_list[95], max(eke_mean)-np.mean(eke_mean)/4,'Autumn',color='m')
            ax[0].fill_between(date_list[60:150], eke_mean.min(), eke_mean.max(), facecolor='orange', alpha=0.1)
            ax[0].text(date_list[185], max(eke_mean)-np.mean(eke_mean)/4,'Winter',color='Blue')
            ax[0].fill_between(date_list[150:240], eke_mean.min(), eke_mean.max(), facecolor='cyan', alpha=0.1)
            ax[0].text(date_list[280], max(eke_mean)-np.mean(eke_mean)/4,'Spring',color='Black')
            ax[0].fill_between(date_list[240:330], eke_mean.min(), eke_mean.max(), facecolor='yellow', alpha=0.1)
            ax[0].fill_between(date_list[330:], eke_mean.min(), eke_mean.max(), facecolor='red', alpha=0.1)
            
        ax[0].grid(True)
        ax[0].set_xlim(date_list[0],date_list[-1])
        ax[0].set_ylim(eke_mean.min(), eke_mean.max())

        monthsFmt = plt.DateFormatter("%b")
        ax[0].xaxis.set_major_formatter(monthsFmt)
        if basemap==True:
            map = Basemap(projection='ortho',lat_0=-90,lon_0=-100,resolution='c',ax=ax[1])
            lonmm,latmm=np.meshgrid(lon,lat)
            lonm,latm=map(lonmm,latmm)
            map.drawmeridians(np.arange(0,360,90),labels=[0,0,0,1],fontsize=10)
            map.drawparallels(np.arange(-90,90,30),labels=[1,1,0,0],fontsize=10)
            map.fillcontinents(color='black',lake_color='aqua')
            map.drawcoastlines()
            map.drawcoastlines()
            im=ax[1].pcolormesh(lonm,latm,eke[0,:,:],cmap=cm.cm.amp,vmin=0,vmax=eke_mean.max())
            fig.colorbar(im, orientation='vertical')
    return eke_mean

def sim_EKE_back_seasonal_variation(fileinit,fileend,areamap='',plot=True,hemisphere='',basemap=True,days=''):
    index=0
    if days=='':
        days=365
    eke_mean=np.zeros(days)
    for ii in range(fileinit,fileend):
        ekefile=Dataset('/home/156/jm5970/notebooks/traceddy/data.input/eke_back_'+str(ii)+'.nc')
        lon=ekefile.variables['Longitude'][:]
        lat=ekefile.variables['Latitude'][:]
        #print(len(lon),len(lat))
        if areamap=='':
            areamap=np.array([[0,len(lon)],[0,len(lat)]])
        lon=lon[areamap[0,0]:areamap[0,1]]
        lat=lat[areamap[1,0]:areamap[1,1]]
        
        eke=np.squeeze(ekefile.variables['EKE_eddy'])
        for tt in range(0,np.shape(eke)[0]):
            eket=eke[tt,:,:]
            eket[eket==0]=np.nan
            eke_mean[index]=np.nanmean(eket[:,:])
            index=index+1
    if plot==True:        
    
        numdays=len(eke_mean)
        base = datetime.datetime(1992, 1, 1, 0, 0)
        date_list = [base + datetime.timedelta(days=x) for x in range(0, numdays)]
        if basemap==True:
            fig, ax = plt.subplots(1,2,figsize=(18,3),gridspec_kw = {'width_ratios':[4, 1]})
        else:
            fig, ax = plt.subplots(1,1,figsize=(18,3))
            ax=[ax]
        #gs = gridspec.GridSpec(1,2, width_ratios=[3, 1]) 
        ax[0].plot(date_list,eke_mean,'-')
        if hemisphere=='North':
            ax[0].text(date_list[20], max(eke_mean)-np.mean(eke_mean)/4,'Winter',color='blue')
            ax[0].fill_between(date_list[0:60], eke_mean.min(), eke_mean.max(), facecolor='cyan', alpha=0.1)
            ax[0].text(date_list[95], max(eke_mean)-np.mean(eke_mean)/4,'Spring',color='black')
            ax[0].fill_between(date_list[60:150], eke_mean.min(), eke_mean.max(), facecolor='yellow', alpha=0.1)
            ax[0].text(date_list[185], max(eke_mean)-np.mean(eke_mean)/4,'Summer',color='red')
            ax[0].fill_between(date_list[150:240], eke_mean.min(), eke_mean.max(), facecolor='red', alpha=0.1)
            ax[0].text(date_list[280], max(eke_mean)-np.mean(eke_mean)/4,'Autumn',color='m')
            ax[0].fill_between(date_list[240:330], eke_mean.min(), eke_mean.max(), facecolor='orange', alpha=0.1)
            ax[0].fill_between(date_list[330:], eke_mean.min(), eke_mean.max(), facecolor='cyan', alpha=0.1)
        else:
            ax[0].text(date_list[20], max(eke_mean)-np.mean(eke_mean)/4,'Summer',color='red')
            ax[0].fill_between(date_list[0:60], eke_mean.min(), eke_mean.max(), facecolor='red', alpha=0.1)
            ax[0].text(date_list[95], max(eke_mean)-np.mean(eke_mean)/4,'Autumn',color='m')
            ax[0].fill_between(date_list[60:150], eke_mean.min(), eke_mean.max(), facecolor='orange', alpha=0.1)
            ax[0].text(date_list[185], max(eke_mean)-np.mean(eke_mean)/4,'Winter',color='Blue')
            ax[0].fill_between(date_list[150:240], eke_mean.min(), eke_mean.max(), facecolor='cyan', alpha=0.1)
            ax[0].text(date_list[280], max(eke_mean)-np.mean(eke_mean)/4,'Spring',color='Black')
            ax[0].fill_between(date_list[240:330], eke_mean.min(), eke_mean.max(), facecolor='yellow', alpha=0.1)
            ax[0].fill_between(date_list[330:], eke_mean.min(), eke_mean.max(), facecolor='red', alpha=0.1)
            
        ax[0].grid(True)
        ax[0].set_xlim(date_list[0],date_list[-1])
        ax[0].set_ylim(eke_mean.min(), eke_mean.max())

        monthsFmt = plt.DateFormatter("%b")
        ax[0].xaxis.set_major_formatter(monthsFmt)
        if basemap==True:
            map = Basemap(projection='ortho',lat_0=-90,lon_0=-100,resolution='c',ax=ax[1])
            lonmm,latmm=np.meshgrid(lon,lat)
            lonm,latm=map(lonmm,latmm)
            map.drawmeridians(np.arange(0,360,90),labels=[0,0,0,1],fontsize=10)
            map.drawparallels(np.arange(-90,90,30),labels=[1,1,0,0],fontsize=10)
            map.fillcontinents(color='black',lake_color='aqua')
            map.drawcoastlines()
            map.drawcoastlines()
            im=ax[1].pcolormesh(lonm,latm,eke[0,:,:],cmap=cm.cm.amp,vmin=0,vmax=eke_mean.max())
            fig.colorbar(im, orientation='vertical')
    return eke_mean

def sim_EKE_seasonal_variation(fileinit,fileend,areamap='',plot=True,hemisphere='',basemap=True,days=''):
    index=0
    if days=='':
        days=365
    eke_mean=np.zeros(days)
    for ii in range(fileinit,fileend):
        ekefile=Dataset('/home/156/jm5970/notebooks/traceddy/data.input/eke_'+str(ii)+'.nc')
        lon=ekefile.variables['Longitude'][:]
        lat=ekefile.variables['Latitude'][:]
        #print(len(lon),len(lat))
        if areamap=='':
            areamap=np.array([[0,len(lon)],[0,len(lat)]])
        lon=lon[areamap[0,0]:areamap[0,1]]
        lat=lat[areamap[1,0]:areamap[1,1]]
        
        eke=np.squeeze(ekefile.variables['EKE'])
        for tt in range(0,np.shape(eke)[0]):
            eket=eke[tt,:,:]
            eket[eket==0]=np.nan
            eke_mean[index]=np.nanmean(eket[:,:])
            index=index+1
    if plot==True:        
    
        numdays=len(eke_mean)
        base = datetime.datetime(1992, 1, 1, 0, 0)
        date_list = [base + datetime.timedelta(days=x) for x in range(0, numdays)]
        if basemap==True:
            fig, ax = plt.subplots(1,2,figsize=(18,3),gridspec_kw = {'width_ratios':[4, 1]})
        else:
            fig, ax = plt.subplots(1,1,figsize=(18,3))
            ax=[ax]
        #gs = gridspec.GridSpec(1,2, width_ratios=[3, 1]) 
        ax[0].plot(date_list,eke_mean,'-')
        if hemisphere=='North':
            ax[0].text(date_list[20], max(eke_mean)-np.mean(eke_mean)/4,'Winter',color='blue')
            ax[0].fill_between(date_list[0:60], eke_mean.min(), eke_mean.max(), facecolor='cyan', alpha=0.1)
            ax[0].text(date_list[95], max(eke_mean)-np.mean(eke_mean)/4,'Spring',color='black')
            ax[0].fill_between(date_list[60:150], eke_mean.min(), eke_mean.max(), facecolor='yellow', alpha=0.1)
            ax[0].text(date_list[185], max(eke_mean)-np.mean(eke_mean)/4,'Summer',color='red')
            ax[0].fill_between(date_list[150:240], eke_mean.min(), eke_mean.max(), facecolor='red', alpha=0.1)
            ax[0].text(date_list[280], max(eke_mean)-np.mean(eke_mean)/4,'Autumn',color='m')
            ax[0].fill_between(date_list[240:330], eke_mean.min(), eke_mean.max(), facecolor='orange', alpha=0.1)
            ax[0].fill_between(date_list[330:], eke_mean.min(), eke_mean.max(), facecolor='cyan', alpha=0.1)
        else:
            ax[0].text(date_list[20], max(eke_mean)-np.mean(eke_mean)/4,'Summer',color='red')
            ax[0].fill_between(date_list[0:60], eke_mean.min(), eke_mean.max(), facecolor='red', alpha=0.1)
            ax[0].text(date_list[95], max(eke_mean)-np.mean(eke_mean)/4,'Autumn',color='m')
            ax[0].fill_between(date_list[60:150], eke_mean.min(), eke_mean.max(), facecolor='orange', alpha=0.1)
            ax[0].text(date_list[185], max(eke_mean)-np.mean(eke_mean)/4,'Winter',color='Blue')
            ax[0].fill_between(date_list[150:240], eke_mean.min(), eke_mean.max(), facecolor='cyan', alpha=0.1)
            ax[0].text(date_list[280], max(eke_mean)-np.mean(eke_mean)/4,'Spring',color='Black')
            ax[0].fill_between(date_list[240:330], eke_mean.min(), eke_mean.max(), facecolor='yellow', alpha=0.1)
            ax[0].fill_between(date_list[330:], eke_mean.min(), eke_mean.max(), facecolor='red', alpha=0.1)
            
        ax[0].grid(True)
        ax[0].set_xlim(date_list[0],date_list[-1])
        ax[0].set_ylim(eke_mean.min(), eke_mean.max())

        monthsFmt = plt.DateFormatter("%b")
        ax[0].xaxis.set_major_formatter(monthsFmt)
        if basemap==True:
            map = Basemap(projection='ortho',lat_0=-90,lon_0=-100,resolution='c',ax=ax[1])
            lonmm,latmm=np.meshgrid(lon,lat)
            lonm,latm=map(lonmm,latmm)
            map.drawmeridians(np.arange(0,360,90),labels=[0,0,0,1],fontsize=10)
            map.drawparallels(np.arange(-90,90,30),labels=[1,1,0,0],fontsize=10)
            map.fillcontinents(color='black',lake_color='aqua')
            map.drawcoastlines()
            map.drawcoastlines()
            im=ax[1].pcolormesh(lonm,latm,eke[0,:,:],cmap=cm.cm.amp,vmin=0,vmax=eke_mean.max())
            fig.colorbar(im, orientation='vertical')
    return eke_mean