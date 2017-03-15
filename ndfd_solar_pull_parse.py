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

def utc_to_local(utc_dt,tzRegion):
    #This should account for timezone and CST/CDT and MST/MDT
    if (tzRegion == 'PSCO'):
        tzR= pytz.timezone('America/Denver')
    else:
        tzR= pytz.timezone('America/Chicago')
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=tzR)
   
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
    for l in f:
        l=l.replace("\n","")
        l=l.replace("vt=","")
        l=l.replace("val=","")
        j = l.split(':')
        print(j)
        vtutcDate = datetime.datetime.strptime(j[2],'%Y%m%d%H')
        print(vtutcDate) 
        vtDate = utc_to_local(vtutcDate,opName)
        print(vtDate)
        #creating a nested list with the datetime and values
        #i.e. [[datetime.datetime(2016, 7, 20, 12, 0), ['44', '26']], [datetime.datetime(2016, 7, 20, 13, 0), ['43', '26']]]
        datList = [vtDate,j[3].split(',')[2] ]
        solarData.append(datList)
    f.close()
    global newSolar
    #create a new 7 X 25 matrix for date and skycover data
    newSolar = [[0 for col in range(25)] for row in range(7)]
    singleSolar = []
    flag=0
    for x in solarData:
        dayCt =  x[0].date() - datetime.date.today()
        dateHour = x[0].hour 
        #newSolar[dayCt.days][0] = x[0].date() 
        if(flag ==0):
        #    newSolar[dayCt.days][(x[0].hour)+1] = float(x[1])/100
            saveDatetime=x[0]
            saveSky = float(x[1])/100
            flag=1
        else:
            diffhours = x[0] - saveDatetime
            if (diffhours.seconds/3600 > 1):
                i=0
                #while(i < int(diffhours.seconds/3600) & (dateHour+i<25)):
                while( i < int(diffhours.seconds/3600) ):
                    i+=1
                    sky = ((float(x[1]) + saveSky)/2)/100
         #           newSolar[dayCt.days][dateHour-i] = sky
            else: 
         #       newSolar[dayCt.days][dateHour+1] = float(x[1])/100 
            saveDatetime=x[0]
            saveSky=float(x[1])

    print(newSolar)
#        print(x)
#        if (flag == 0):
#            saveDatetime=x[0]
#            flag=1    
#        diffhours = x[0] - saveDatetime
#        dayCt =  x[0].date() - datetime.date.today()
#        dateHour = x[0].hour 
#        i=0
#        newSolar[dayCt.days][0]=x[0].date()
        #this section fills in the gaps when the forecast changes from hourly to 3 hour intervals
#        while (i < int(diffhours.seconds/3600)):
#            incDate = saveDatetime + datetime.timedelta(hours=i)
#            if (i == 0):
#                sky = saveSky/100.0
#            else:
#                sky = ((float(x[1][0]) + saveSky)/2)/100.0
            #print(dayCt.days,dateHour,i,dateHour+i)
#            newSolar[dayCt.days][dateHour+i]= sky
#            i += 1
#        saveDatetime=x[0]
#        saveSky = float(x[1][0])

#solarMaxGen looks in the max generation 'csv' files by farm and pulls the current date plus 7 days
#resulting in a 25X7 array
def solarMaxGen(sPlant):
    f = open(mainPath+sPlant+'.csv','r')
    nowDate = datetime.datetime.now().date()
    plus7Date = nowDate +datetime.timedelta(days=6)
    solarmax = [[0 for col in range(25)] for row in range(7)]
    ct=rowct=0
    finalSolar=[]
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
            newSky=(np.array(newSky,dtype=float))
        #multiply the solar radiance times the max solar generation
        finalSolar.append(np.multiply(solar1dayMax,newSky))
     
    solarDF = pd.DataFrame(newSolar)
    finalDF = pd.DataFrame(finalSolar)
    #print(solarDF) 
    #print(finalDF)
    #print(newSolar[0],finalSolar) #skycover
    #print(solarMax)    #maxSolar
    #print(finalSolar)    #finalSolar
        
#the solar meta table is set up such that the nested index matches up with the ndfd sky cover data
#for example Sune1 is in the first nested array of farms and will match up with the first array of skycover data
allRowData = []
#solarPull()
dList=[]
rowCt=0
with open('solarMeta.csv') as region:
    for l in region:
        dList.append(l.strip().split(':'))
        rowCt+=1
    listCt=0
    #rowCt accounts for the number of total rows in the solarMeta.txt file
    #because the meta file is split with regions and names on the first half
    #and location data in the 2nd half, the loop only needs to run through half
    #of the data while the 2nd half is referred to via 'listCt+3'
    while listCt<rowCt/2:
        #for z in range(len(plantData))[1:]:
        for z in range(len(dList[listCt][1:])):
            for y in (dList[listCt][z+1].split(',')):
                print(y)
                if (y is not None):  
                    #def solarParser(opName,sPlant,lon,lat,sCount)
                    solarParser(dList[listCt+3][0],y,dList[listCt+3][z+1].split(',')[0],dList[listCt+3][z+1].split(',')[1],z)
                    solarMaxGen(y)
        listCt+=1    
