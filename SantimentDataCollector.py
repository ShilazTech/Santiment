# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 09:03:45 2018

@author: P.K Tyagi
"""
import numpy
import pandas as pd
from ta import *
from pandas import *
import pandas as pd
import os.path
from os import path
from urllib.request import urlopen, HTTPError
import urllib.parse
from datetime import datetime
from datetime import timedelta
from contextlib import suppress
import csv
import matplotlib.pyplot as plt
import san
from san import Batch
san.ApiConfig.api_key = 'your key'
#print(san.get("projects/erc20"))
#%%
def getDate(timeseries,Interval):
    indx=timeseries.index.get_level_values(0).tolist()      
    dtime=[]
    for k in range(len(indx)):
        x=indx[k]
        if Interval=="1d":
            x=x.strftime("%m/%d/%Y")
        else:
            x=x.strftime("%Y-%m-%d %H:%M:%S")
        dtime.append(x)
    return dtime
def acmsum(inOutDifference):
    newdata=[0 for x in range(len(inOutDifference))]
    for i in range(len(inOutDifference)):
        s=sum(inOutDifference[0:i])
        newdata[i]=s
    return newdata
def datafromSantinent(slugs,filepath,days,Interval):
    data=[]
    now=datetime.utcnow()    
    startdate=datetime.now() - timedelta(days=days)
    now=now.strftime("%Y-%m-%dT%H:%M:%SZ")
    startdate= startdate.strftime("%Y-%m-%dT%H:%M:%SZ")  
    
    for slug in slugs: 
        if slug=="bitcoin": 
            ohlcv=san.get("ohlcv/"+slug,from_date=startdate,to_date=now,interval=Interval) 
            indx1=getDate(ohlcv,Interval)      
            openPriceUsd=ohlcv['openPriceUsd'].tolist()
            closePriceUsd=ohlcv['closePriceUsd'].tolist()
            highPriceUsd=ohlcv['highPriceUsd'].tolist()
            lowPriceUsd=ohlcv['lowPriceUsd'].tolist()
            volume=ohlcv['volume'].tolist()
            marketcap=ohlcv['marketcap'].tolist() 
            
            batch = Batch()                
            batch.get("social_volume/"+slug,from_date=startdate,to_date=now,interval=Interval)    
            [social_volume] = batch.execute()
            try:
                indx6=getDate(social_volume,Interval)
                mentionsCount = social_volume['mentionsCount'].tolist()
            except:
                indx6=indx1
                mentionsCount=[]

            
            datapoints=len(indx1)
            data = [[0 for x in range(13)] for y in range(datapoints)] 
            fl=filepath+slug  
            try:
                with open(fl, 'r') as f: #open the file 
                    f.close()
                fileexists=1
            except:
                fileexists=0        
            for i in range(datapoints):
                #print(i)
                if i==0:
                    if path.exists(fl):
                        print("file exists  ", fl)
                    else:
                        data[i][0]="Ticker"
                        data[i][1]="Date"            
                        data[i][2]="open"
                        data[i][3]="close"
                        data[i][4]="high"
                        data[i][5]="low"
                        data[i][6]="volume"        
                        data[i][7]="marketcap"
                        data[i][8]="outInDifference"
                        data[i][9]="activeAddresses"
                        data[i][10]="burnRate"
                        data[i][11]="activity"
                        data[i][12]="mentionsCount"
                else:            
                    data[i][0]=slug
                    data[i][1]=indx1[i-1]
                    data[i][2]=openPriceUsd[i-1]
                    data[i][3]=closePriceUsd[i-1]
                    data[i][4]=highPriceUsd[i-1]
                    data[i][5]=lowPriceUsd[i-1]
                    data[i][6]=volume[i-1]        
                    data[i][7]=marketcap[i-1] 
                    data[i][8]=0
                    data[i][9]=0
                    data[i][10]=0
                    data[i][11]=0
                    try:
                        k=0                   
                        while k<=len(indx6):
                            #print(indx1[i-1], indx5[k])
                            if indx1[i-1] == indx6[k]:
                                data[i][12]=mentionsCount[k]
                                da=mentionsCount[k]
                                k=len(indx6)
                            k=k+1                               
                    except:
                        data[i][12]=0
                     
            if path.exists(fl):
                print("File Exists")
                with open('%s.csv' % fl, 'a',newline='') as f:
                    for d in data:
                        writer = csv.writer(f)
                        writer.writerow(d)
            else:   
                print("File Does not Exists")
                with open('%s.csv' % fl, 'w',newline='') as f:                                          
                    for d in data:
                        writer = csv.writer(f)
                        writer.writerow(d)
        else:            
            try:
                batch = Batch()
                batch.get("exchange_funds_flow/"+slug,from_date=startdate,to_date=now, interval=Interval)
                batch.get("daily_active_addresses/"+slug,from_date=startdate,to_date=now,interval=Interval)
                batch.get("burn_rate/"+slug,from_date=startdate,to_date=now,interval=Interval)
                batch.get("github_activity/"+slug,from_date=startdate,to_date=now,interval=Interval)
                batch.get("social_volume/"+slug,from_date=startdate,to_date=now,interval=Interval) 
                batch.get("burn_rate/"+slug,from_date=startdate,to_date=now,interval=Interval) 
                [exchange_funds_flow, daily_active_addresses,burn_rate,github_activity,social_volume,burn_rate] = batch.execute()
            except:
                batch = Batch()
                batch.get("exchange_funds_flow/"+slug,from_date=startdate,to_date=now,interval=Interval)
                batch.get("daily_active_addresses/"+slug,from_date=startdate,to_date=now,interval=Interval)
                batch.get("burn_rate/"+slug,from_date=startdate,to_date=now,interval=Interval)
                batch.get("github_activity/"+slug,from_date=startdate,to_date=now,interval=Interval) 
                batch.get("burn_rate/"+slug,from_date=startdate,to_date=now,interval=Interval) 
                [exchange_funds_flow, daily_active_addresses,burn_rate,github_activity,burn_rate] = batch.execute()
            ohlcv=san.get("ohlcv/"+slug,from_date=startdate,to_date=now,interval=Interval)       
            
            indx1=getDate(ohlcv,Interval)      
            openPriceUsd=ohlcv['openPriceUsd'].tolist()
            closePriceUsd=ohlcv['closePriceUsd'].tolist()
            highPriceUsd=ohlcv['highPriceUsd'].tolist()
            lowPriceUsd=ohlcv['lowPriceUsd'].tolist()
            volume=ohlcv['volume'].tolist()
            marketcap=ohlcv['marketcap'].tolist() 
            indx2=getDate(exchange_funds_flow,Interval)
            inOutDifference = exchange_funds_flow['inOutDifference'].tolist()
            #inOutDifference=acmsum(inOutDifference)
            indx3=getDate(daily_active_addresses,Interval)
            activeAddresses = daily_active_addresses['activeAddresses'].tolist()
            indx4=getDate(burn_rate,Interval)
            burnRate = burn_rate['burnRate'].tolist()
            
            try:
                indx5=getDate(github_activity,Interval)
                activity = github_activity['activity'].tolist()
            except:
                indx5=indx1
                activity=[]
            
            try:
                indx6=getDate(social_volume,Interval)
                mentionsCount = social_volume['mentionsCount'].tolist()
            except:
                indx6=indx1
                mentionsCount=[]
        datapoints=len(indx1)
        data = [[0 for x in range(13)] for y in range(datapoints)] 
        fl=filepath+slug  
        try:
            with open(fl, 'r') as f: #open the file 
                f.close()
            fileexists=1
        except:
            fileexists=0        
        for i in range(datapoints):
            #print(i)
            if i==0:
                if path.exists(fl):
                    print("file exists  ", fl)
                else:
                    data[i][0]="Ticker"
                    data[i][1]="Date"            
                    data[i][2]="open"
                    data[i][3]="close"
                    data[i][4]="high"
                    data[i][5]="low"
                    data[i][6]="volume"        
                    data[i][7]="marketcap"
                    data[i][8]="outInDifference"
                    data[i][9]="activeAddresses"
                    data[i][10]="burnRate"
                    data[i][11]="activity"
                    data[i][12]="mentionsCount"
                    
            else:            
                data[i][0]=slug
                data[i][1]=indx1[i-1]
                data[i][2]=openPriceUsd[i-1]
                data[i][3]=closePriceUsd[i-1]
                data[i][4]=highPriceUsd[i-1]
                data[i][5]=lowPriceUsd[i-1]
                data[i][6]=volume[i-1]        
                data[i][7]=marketcap[i-1] 
                try:
                    k=0                   
                    while k<=len(indx2):
                        #print(indx1[i-1], indx5[k])
                        if indx1[i-1] == indx2[k]:
                            data[i][8]=-inOutDifference[k]
                            da=-inOutDifference[k]
                            k=len(indx2)
                        k=k+1                               
                except:
                    data[i][8]=0 
                try:
                    k=0                   
                    while k<=len(indx3):
                        #print(indx1[i-1], indx5[k])
                        if indx1[i-1] == indx3[k]:
                            data[i][9]=activeAddresses[k]
                            da=activeAddresses[k]
                            k=len(indx3)
                        k=k+1                               
                except:
                    data[i][9]=0  
                try:
                    k=0                   
                    while k<=len(indx4):
                        #print(indx1[i-1], indx5[k])
                        if indx1[i-1] == indx4[k]:
                            data[i][10]=burnRate[k]
                            da=burnRate[k]
                            k=len(indx4)
                        k=k+1                               
                except:
                    data[i][10]=0  
                try:
                    k=0                   
                    while k<=len(indx5):
                        #print(indx1[i-1], indx5[k])
                        if indx1[i-1] == indx5[k]:
                            data[i][11]=activity[k]
                            da=activity[k]
                            k=len(indx5)
                        k=k+1                               
                except:
                    data[i][11]=0
                try:
                    k=0                   
                    while k<=len(indx6):
                        #print(indx1[i-1], indx5[k])
                        if indx1[i-1] == indx6[k]:
                            data[i][12]=mentionsCount[k]
                            da=mentionsCount[k]
                            k=len(indx6)
                        k=k+1                               
                except:
                    data[i][12]=0
               
        if path.exists(fl):
            print("File Exists")
            with open('%s.csv' % fl, 'a',newline='') as f:
                for d in data:
                    writer = csv.writer(f)
                    writer.writerow(d)
        else:   
            print("File Does not Exists")
            with open('%s.csv' % fl, 'w',newline='') as f:                                          
                for d in data:
                    writer = csv.writer(f)
                    writer.writerow(d)

#%%        
#%% Main Program and parameters
slugs=["bitcoin","ethereum","binance-coin","omisego","augur","maker","mithril","kucoin-shares","wax","bancor","loopring","decentraland","digixdao","dentacoin","crypto-com","funfair","storj","sonm","sirin-labs-token", "mobilego","huobi-token","indorse-token","aragon","power-ledger","tenx","kyber-network","salt","civic","singularitynet","santiment","singulardtv","0x","aeternity","basic-attention-token","bytom","golem-network-tokens","chainlink","populous","status","waltonchain","aion"]
filepath="define your file path"
days=365 ## how many days dat to be collected
Interval="1d" ## time interval
datafromSantinent(slugs,filepath,days, Interval)

    