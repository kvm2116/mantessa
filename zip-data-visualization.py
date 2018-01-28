"""
Created on Wed Sep 27 19:56:53 2017

@author: akutn


Converts JSON from ip-state-scraper to JSONS for visualizations

To change for next use:
    outageFilename
"""

import json
import csv
import sys 

def compute_viz(geojson_file_path, ipscore_file_path):
    #directory = input("Enter the directory of the origionnal .json")
    filename = geojson_file_path
    jsonToCopy=""
    with open (filename) as data:
        jsonToCopy=data.readline()

        
    outageFilename=ipscore_file_path
    mappedZips={}
    timestamp=""
    with open (outageFilename) as data:
        csvReader= csv.reader(data,delimiter=",",quotechar='"')
        output = mapZips(csvReader)
        mappedZips=output[0]
        timestamp = output[1]

    makeNJson(mappedZips,timestamp, jsonToCopy)
        
def mapZips(csvReader):
    zipToNumUp={}
    zipToTotIP={}
    first = True
    timestamp=""
    for row in csvReader:
        if first:
            timestamp = row[4]
            first=False
        elif(len(row)>0):
            zip = row[3]
            if zip not in zipToTotIP:
                zipToTotIP[zip]=0
                zipToNumUp[zip]=0
                
            zipToTotIP[zip]+=1
            
            if(row[4]):
                zipToNumUp[zip]+=1
    zipToPerUp={}
    for zip in zipToTotIP:
        zipToPerUp[zip]=zipToNumUp[zip]/zipToTotIP[zip]
    return (zipToPerUp,timestamp)


def makeNJson(mappedZips,timestamp, jsonToCopy):
    #TODO write to wherever the server reads from 
    writeTo=open('current-scores.json','w+')
    j=json.loads(jsonToCopy)
    index=0
    for feat in j['features']:
        zip=feat['properties']['geoid10']
        if zip in mappedZips.keys():
            j['features'][index]['properties']['perUP']=mappedZips[zip]
        index+=1
    json.dump(j,writeTo)
    writeTo.close()
