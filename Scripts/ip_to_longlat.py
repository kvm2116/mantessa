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
import json
import math
import csv

reader = db.Reader('./GeoIP2-City.mmdb')

ip_locations = {}
invalidC = 0

with open ('20170207.json', 'r') as ips, open('static.csv', 'w') as f:
	csv_static = csv.writer(f)

	for line in ips:
		data = json.loads(line)
		try: 
			response = reader.city(data['ip'])
		except geoip2.errors.AddressNotFoundError: 
			invalidC += 1
			continue 
		lat = response.location.latitude
		lon = response.location.longitude

		if math.isclose(float(data['location']['latitude']), lat, rel_tol=1e-4) and math.isclose(float(data['location']['longitude']), lon, rel_tol=1e-4):
			csv_static.writerow((data['ip'], lat, lon))
			
		# print("C: " + str(data['location']['latitude']) + " MM: " + str(lat))
		# print("C: " + str(data['location']['longitude']) + " MM: " + str(lon)) 	
