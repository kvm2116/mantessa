"""
This is a python script to convert create a whitelist of sorted IPs, and incudes lat, lon, city

Author: Niloofar Bayat
        (nb2776@columbia.edu)
"""
from netaddr import *
import csv
import socket
import pandas
import geoip2.database as db
import geoip2
import math
import csv
import sys
import os.path
import struct

def ip2int(addr1, addr2):
    #return struct.unpack("!I", socket.inet_aton(addr))[0]    
    ip1 = long(0)
    ip2 = long(0)
    try:
        ip1 = long(IPAddress(unicode(addr1, "utf-8")))
        ip2 = long(IPAddress(unicode(addr2, "utf-8")))
    except core.AddrFormatError:
        return (None,None)
    return (ip1, ip2)

def int2ip(addr):
    return socket.inet_ntoa(struct.pack("!I", addr))


reader = db.Reader(sys.argv[1])

ip_locations = {}
invalidC = 0

with open('CCCS_sorted.csv', 'r') as f1, open ('sorted_output.csv', 'w') as f2:
    csv_reader = csv.reader(f1, delimiter=',')
    csv_static = csv.writer(f2)
    result = []

    for line in csv_reader:
        data = int2ip(long(float(line[0])))
          
        try:
            response = reader.city(data[0])
        except:# (geoip2.errors.AddressNotFoundError, ValueError): 
            invalidC += 1 
            continue
        lat = response.location.latitude
        lon = response.location.longitude
        if lat is None or lon is None:
                continue
        city =  response.city.name
        if city: city = city.encode("utf-8")
        else: city = '' 
    
        csv_static.writerow([line, lat, lon, response.postal.code, response.subdivisions.most_specific.iso_code, city])
