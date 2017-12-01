'''
Joshua Zweig

This python script is a tool for helping determine some of the IP addresses
that we might want to include in the static set.
The GeoIP2-City MaxMind data base stores IP location data from 6 months ago.
The locations stored in that database are being copmared against current IP location
data. Any lat,longs that have not changed in the last 6 months are written to a CSV, 
as they are likely candidates for IPs that are stationary and that we will be able 
to map with confidence to a substation

'''

import pandas 
import geoip2.database as db
import geoip2
import math
import csv
import sys
import os.path

reader = db.Reader(sys.argv[1])

ip_locations = {}
invalidC = 0


with open('nell/USData/DateDat', 'r') as DateDat:
	for line in DateDat:
		line = line.strip()
		src = 'nell/USData/' + line + '.csv'
		print(src)
		dst = 'nell/USconverted/' + line + '.csv'
		print(dst)
		if os.path.isfile(src) and not os.path.isfile(dst):
			with open (src, 'r') as ips, open(dst, 'w') as f:
				csv_reader = csv.reader(ips, delimiter=',', quotechar='|')
				csv_static = csv.writer(f)
	
				for i, data in enumerate(csv_reader):
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

					csv_static.writerow([data[0], lat, lon, response.postal.code, response.subdivisions.most_specific.iso_code, city]) 

