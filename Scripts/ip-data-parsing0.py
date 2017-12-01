# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 13:07:11 2017

@author: akutn
"""
import csv
import os
import json
from urllib.request import urlopen

#from geopy.geocoders import Nominatim
#geolocator = Nominatim()
import pytz, datetime
"""
def findCounty(longitude, latitude):
    location = geolocator.reverse(longitude+","+latitude)
    print (location.raw)
    return ""
    """
    
def findCounty(lon, lat):

    url = "https://maps.googleapis.com/maps/api/geocode/json?"
    url += "latlng=%s,%s&sensor=false&key=AIzaSyBrTt_3tu0gM4XJwhTxbISC7wSoZRVGi3g" % (lat, lon)
    #c=httplib.HTTPSConnection(url)
    #c.request("GET","/")
    #v=c.getresponse.read()
    v = urlopen(url).read()
    j = json.loads(v)
    components = j['results'][0]['address_components']
    county="Not Found"
    for i in components:
        if str(i).find('administrative_area_level_2')!=-1:
            county = i['long_name']
    print(county)
    return county
    

def makeStdTime(tm):
    gmt = pytz.timezone('GMT')
    est = pytz.timezone('US/Eastern')
    year = tm[0:4]
    month= tm[4:6]
    day = tm[6:8]
    tym=month+"/"+day+"/"+year+" "+tm[9:17]
    fmt='%m/%d/%Y %H_%M_%S'
    date = datetime.datetime.strptime(tym, fmt)
    date = gmt.localize(date)
    fTime = date.astimezone(est)
    newFmt='%m/%d/%Y %H:%M'
    return fTime.strftime(newFmt)

directory=input("Enter the directory")
#directory_in_str="/local/mantessa/irma-data/"
info=[]
filename= "ips-annotated.txt"
with open(directory+"/"+filename) as data:
    info=data.readlines()
writeTo=open('scan-irma-data.csv','w')
writer = csv.writer(writeTo, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
countiesCustomers = {}#ip => county
countiesTot={}#county=> total IP in county
for line in info:
    ln=line.split(",")
    long = ln[1]
    lat = ln[2]
    county = findCounty(long,lat)
    ip=ln[0]
    countiesCustomers[ip]=county
    if county in countiesTot.keys():
        countiesTot[county]+=1
    else:
        countiesTot[county] = 1
    
directory_of_data=input("Enter data directory:" )
countiesNumUp={}#county=> total county up
for file in os.listdir(directory_of_data):
    filename=os.fsdecode(file)
    with open(directory_of_data+"\\"+filename) as ips:
        lsIP=ips.readlines()
    
    for county in countiesTot.keys():#sets all counties up to 0
        countiesNumUp[county]=0
        print (county)
        
        
    for ip in lsIP:#find's associated ip with county and increments
        ip=ip.replace('\n',"")
        county = countiesCustomers[ip]
        countiesNumUp[county]+=1
    
    
    for county in countiesTot.keys():
        timestamp=makeStdTime(filename)#plus some function?
        writer.writerow([county,timestamp,str(countiesNumUp[county]),str(countiesTot[county])])
        
writeTo.close()
            
    
    
        