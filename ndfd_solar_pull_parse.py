#!/home/bglr02/anaconda3/bin/python3

import time
import dateutil.parser
import datetime
from datetime import timedelta
import numpy as np
from datetime import timezone
import pytz
import urllib.request
import shutil
import subprocess
import shlex
import os 
import pandas as pd

#filenames=['/metero/morningscripts/solar/SPS_solar.txt','/metero/morningscripts/solar/SCO_solar.txt']
#filenames=['/metero/morningscripts/solar/PSCO_solar.txt']
mainPath = '/metero/morningscripts/solar/'

'''
function utc_to_local
many issues with date and time.  This accounts for time shifts, but only accounts for the timezone,
and does not deal with the daylight savings time change issue
'''
def utc_to_local(utc_dt,tzRegion):
    #This should account for timezone and CST/CDT and MST/MDT
    if (tzRegion == 'PSCO'):
        tzR= pytz.timezone('America/Denver')
    else:
        tzR= pytz.timezone('America/Chicago')
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=tzR)

'''
function solarPull
This function needed to go through a proxy firewall to pull the data from 
weather.noaa.gov and pull the cloud cover data from the models
'''   
def solarPull():
    proxydata = open('/metero/morningscripts/proxyfile', 'r')
    ct=0
    for i in proxydata:
        i=i.replace('\n','')
        if ct==0:
            xceluser=i
        if ct==1:
            xcelpw=i
        ct+=1
    proxyurl = 'http://'+xceluser+':'+xcelpw+'@wproxy.corp.xcelenergy.com:8080'
    proxy = urllib.request.ProxyHandler({'http': proxyurl})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    urlList=['http://weather.noaa.gov/pub/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/VP.001-003/',
             'http://weather.noaa.gov/pub/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/VP.004-007/']

    #attempted to use smaller files by region, but the files don't appear to contain the same amount of data
    #maybe something to dig into later
    #urlList=[
    #         'http://weather.noaa.gov/pub/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.splains/VP.001-003/',
    #         'http://weather.noaa.gov/pub/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.splains/VP.004-007/',
    #         'http://weather.noaa.gov/pub/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crplains/VP.001-003/',
    #         'http://weather.noaa.gov/pub/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crplains/VP.004-007/',
    #         'http://weather.noaa.gov/pub/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/VP.001-003/',
    #         'http://weather.noaa.gov/pub/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/VP.004-007/'
    #        ]
    ct=0
    file='ds.sky.bin'
    
    #opcoList=['SPS','SPS','PSCO','PSCO','NSP','NSP']
    for url in urlList:
        wUrl=url+file
        req = urllib.request.urlopen(wUrl)
    #    filename=mainPath+'ds.sky.'+opcoList[ct]+'.'+str(ct)+'.bin'
        filename=mainPath+'ds.sky.'+str(ct)+'.bin'
        ct+=1
        with open(filename, 'wb') as fp:
            shutil.copyfileobj(req,fp)

'''
function solarParser 
'''       
def solarParser(opName,sPlant,lon,lat,sCount):
    wgribString = 'wgrib2 '+mainPath+'ds.sky.0.bin -vt -lon '+lon+' '+lat 
    wgribString2 = 'wgrib2 '+mainPath+'ds.sky.1.bin -vt -lon '+lon+' '+lat 
    #subprocess.call(shlex.split('wgrib2 /metero/morningscripts/solar/ds.sky1.bin -vt -lon -105.88 37.77 -csv junk' ))
    #subprocess.call(shlex.split(wgribString))
    #subprocess.call(shlex.split(wgribString2))
    with open(mainPath+opName+'_solar.txt', "w") as outfile:
        subprocess.call(shlex.split(wgribString), stdout=outfile)
        subprocess.call(shlex.split(wgribString2),stdout=outfile)  
    outfile.close()
 
    fname=mainPath+opName+'_solar.txt'
    solarData=[]
    f = open(fname,'r')
    lineCt=0
    solarData = [[0 for col in range(4)] for row in range(7*24)]
    #fill in the first part of the data set
    for j in range(len(solarData)):
        if (j < 23) :
            solarData[j][3]=j
    for l in f:
        l=l.replace("\n","")
        l=l.replace("vt=","")
        l=l.replace("val=","")
        j = l.split(':')
        dateHourDiff = 0 
        vtutcDate = datetime.datetime.strptime(j[2],'%Y%m%d%H')
        vtDate = utc_to_local(vtutcDate,opName)
        vtSky = int(j[3].split(',')[2])
        #print(l,vtutcDate,vtDate,vtSky,vtDate.hour)
        if (lineCt == 0 ) :
            lineCt = int(vtDate.hour)
            dateNow =  datetime.datetime.now().date()
            ndfdDate = vtDate.date()
            solarData[lineCt][0] = utc_to_local(vtDate,opName)
            solarData[lineCt][2] = lineCt
            solarData[lineCt][3] = lineCt
            solarData[lineCt][1] = vtSky/100
            if (dateNow != ndfdDate):
                return ('Date not Valid.  Try Again!')
        else:
            dateHourDiff =  int(((vtDate - savevtDate).seconds) / 3600)
            lineCt = lineCt + dateHourDiff
            while (savelineCt < lineCt):
                savelineCt += 1
                savevtDate += timedelta(hours=1)
                #print(l,vtutcDate,vtDate,savelineCt,savevtDate.hour)
                solarData[savelineCt][0] = savevtDate
                solarData[savelineCt][2] = lineCt
                solarData[savelineCt][3] = savevtDate.hour
                if (savelineCt == lineCt):
                    solarData[savelineCt][1] = vtSky/100
                else:
                    solarData[savelineCt][1] = ((vtSky+savevtSky)/2)/100
        savevtDate = vtDate
        savelineCt = lineCt
        savevtSky = vtSky
    #if you need to fill in the more hours of data past 163 
    #if (lineCt == 163):
    #    while(savelineCt < 167):
    #        savelineCt += 1
    #        vtutcDate+=timedelta(hours=1)
    #        solarData[savelineCt][0]= utc_to_local(vtutcDate,opName)
    #        solarData[savelineCt][1]=savevtSky/100
    #        solarData[savelineCt][2]=lineCt
    #        solarData[savelineCt][3]= int(utc_to_local(vtutcDate,opName).hour)

    newsolarDF = pd.DataFrame(solarData)
    #print(newsolarDF)
    f.close()
    global newSolar
    #create a new 7 X 25 matrix for date and skycover data
    newSolar = [[0 for col in range(25)] for row in range(7)]
    flag=0
    for x in solarData:
        #print(x)
        try:
            if (isinstance( x[0] , int)):
                x[0] = dateNow
                dayCt = 0
            else:
                x[0] = x[0].date()
                dayCt = (x[0] - dateNow).days
            if (x[3] == 0) :
                newSolar[dayCt][0] = x[0]
                newSolar[dayCt][x[3]+1] = x[1]
            else:
                newSolar[dayCt][x[3]+1] = x[1]
        except:
           print('exception') 
    #print(newSolar)

#solarMaxGen looks in the max generation 'csv' files by farm and pulls the current date plus 7 days
#resulting in a 25X7 array
def solarMaxGen(sOpCo,sPlant):
    f = open(mainPath+'solarDailyMax/'+sPlant+'.csv','r')
    nowDate = datetime.datetime.now().date()
    plus7Date = nowDate +datetime.timedelta(days=6)
    solarmax = [[0 for col in range(25)] for row in range(7)]
    ct=rowct=0
    finalSolar = []
    for l in f:
        l = l.replace("\n","")
        j = l.split(',')
        #need to skip the header
        if (ct>0):
            maxPVDate = datetime.datetime.strptime(j[0],'%m/%d/%Y').date()
            if (nowDate <= maxPVDate <= plus7Date):
                solarmax[rowct][0] = maxPVDate
                for pv in range(len(j[3:])):
                    solarmax[rowct][pv+1] = j[pv+3]
                rowct+=1
        ct+=1
    for rowNum in range(len(solarmax)):
        if (solarmax[rowNum][0] == newSolar[rowNum][0]):
            solar1dayMax=(np.array(solarmax[rowNum][1:],dtype=float))
            #apply sky coverage to solar radiance
            newSky = [(1-(0.67*n**2)+(0.35*n)) if (1-(0.67*n**2)+(0.35*n))>0 else 0 for n in newSolar[rowNum][1:]]
            newSky = (np.array(newSky,dtype=float))
        #multiply the solar radiance times the max solar generation
        finalSolar.append(np.multiply(solar1dayMax,newSky))
    global solar2DF
    solarDF = pd.DataFrame(newSolar)
    solarDF =solarDF.transpose()
    finalDF = pd.DataFrame(finalSolar)
    finalDF = finalDF.transpose()
    solarmax = np.delete(solarmax, 0, axis = 1)
    solarmaxDF = pd.DataFrame(solarmax,dtype=float)
    solarmaxDF = solarmaxDF.transpose()
    #vertically stack dataframes
    solar2DF = pd.concat([solarDF, finalDF], axis = 0)
    solar2DF = pd.concat([solar2DF, solarmaxDF], axis = 0)
    #print(solar2DF)
    #solarDF.to_csv('/metero/morningscripts/solar/OuputFiles/'+sOpCo+'_'+sPlant+'_solar.csv' )
    solar2DF.to_csv('/metero/morningscripts/solar/OutputFiles/'+sOpCo+'_'+sPlant+'_final_solar.csv',header=None)
    
     
    #print(solarDF) 
    #print(finalDF)
    #print(newSolar[0],finalSolar) #skycover
    #print(solarMax)    #maxSolar
    #print(finalSolar)    #finalSolar
        
#the solar meta table is set up such that the nested index matches up with the ndfd sky cover data
#for example Sune1 is in the first nested array of farms and will match up with the first array of skycover data
allRowData = []
solarPull()
dList=[]
rowCt=0
with open('solarMeta.csv') as region:
    for l in region:
        dList.append(l.strip().split(':'))
        rowCt+=1
    listCt=0
    advanceBy = int((rowCt+1)/2)
    #rowCt accounts for the number of total rows in the solarMeta.txt file
    #because the meta file is split with regions and names on the first half
    #and location data in the 2nd half, the loop only needs to run through half
    #of the data while the 2nd half is referred to via 'listCt+advanceBy'
    while listCt<rowCt/2:
        regionalsolar = pd.DataFrame()
        solarsum = pd.DataFrame()
        regionFarmCt = 0
        #for z in range(len(plantData))[1:]:
        for z in range(len(dList[listCt][1:])):
            for y in (dList[listCt][z+1].split(',')):
                print(y)
                if (y is not None):  
                    #def solarParser(opName,sPlant,lon,lat,sCount)
                    OpRegion = dList[listCt+advanceBy][0]
                    solarParser(OpRegion,y,dList[listCt+advanceBy][z+1].split(',')[0],dList[listCt+advanceBy][z+1].split(',')[1],z)
                    solarMaxGen(dList[listCt+advanceBy][0],y)
                    solar2sum = solar2DF.reset_index(drop=True)
                    solar2sum.iloc[0,0:]  = 1 
                    solarsum = solarsum.add(solar2sum, fill_value=0)
                    regionalsolar = pd.concat([regionalsolar,solar2DF],axis=1)
                regionFarmCt= regionFarmCt+1 
        #look into df.loc to determine if you can create the sum of every nth column starting at row 1
        regionalsolar = regionalsolar.reset_index(drop=True)
        regionalsolar = pd.concat([regionalsolar,solarsum],axis=1)
        regionalsolar.to_csv('/metero/morningscripts/solar/OutputFiles/'+OpRegion+'_final_solar.csv')
        listCt+=1
    
