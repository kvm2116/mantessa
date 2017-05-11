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

reader = db.Reader('./GeoIP2-City.mmdb')

ip_locations = {}
invalidC = 0

with open ('20170114.csv', 'r') as ips, open('static_20170114e.csv', 'w') as f:
	csv_reader = csv.reader(ips, delimiter=',', quotechar='|')
	csv_static = csv.writer(f)

	for i, data in enumerate(csv_reader):
		if i < 3773958:
			continue
		try: 
			response = reader.city(data[0])
		except:# (geoip2.errors.AddressNotFoundError, ValueError): 
			invalidC += 1
			continue 
		lat = response.location.latitude
		lon = response.location.longitude

		if lat is None or lon is None:
			continue 

		if math.isclose(float(data[1]), float(lat), rel_tol=1e-4) and math.isclose(float(data[2]), float(lon), rel_tol=1e-4):
			csv_static.writerow((data[0], lat, lon))
			
		# print("C: " + str(data['location']['latitude']) + " MM: " + str(lat))
		# print("C: " + str(data['location']['longitude']) + " MM: " + str(lon)) 	
