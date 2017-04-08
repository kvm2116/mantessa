import pandas 
import geoip2.database as db
import geoip2
import json
import csv
import sys

reader = db.Reader('./GeoIP2-City.mmdb')

ip_locations = {}
invalidC = 0

with open (sys.argv[1], 'r') as ips:
	ip_reader = csv.reader(ips)

	for i, add in enumerate(ip_reader):
		if i%50000 is 0:
			print("Processing " + str(i))
		ip = add[0]
		try: 
			response = reader.city(ip)
		except:# geoip2.errors.AddressNotFoundError: 
			invalidC += 1
			continue 
		
		state = response.subdivisions.most_specific.iso_code
		state_file = open("../ip_states/" + str(state) + "_ips.csv", 'a')
		w = csv.writer(state_file)
		w.writerow(add)
		state_file.close() 