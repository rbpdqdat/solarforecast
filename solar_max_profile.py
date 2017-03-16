#!/home/bglr02/anaconda3/bin/python3

import time
import dateutil.parser
import datetime
from datetime import timedelta
import pandas as pd 

mainPath='/metero/morningscripts/solar/'

#This is a nested list in order of the associated ndfd sky cover file
solarfiles=[['Alamosa.csv']]

for fname in solarfiles:
    #newfile= fname.replace('solar.txt','ndfd.csv')
    #nfile = open(newfile, 'w')
    f = open(mainPath+fname,'r')
    nowDate = datetime.datetime.now().date()
    plus7Date = nowDate +datetime.timedelta(days=6)
    ct=0
    solarmax=[]
    for l in f:
        l = l.replace("\n","")
        j = l.split(',')
        if (ct>0):
            maxPVDate = datetime.datetime.strptime(j[0],'%m/%d/%Y').date()
            if (nowDate <= maxPVDate <= plus7Date):
                sList = [maxPVDate,j[3:]]
                solarmax.append(sList) 
        ct+=1
    #nfile.close()
    print(solarmax)
    f.close()

    
