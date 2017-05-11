"""
Author:	nb2776@columbia.edu
		tusharag171@gmail.com/ta2482@columbia.edu


Update Config.py with your censys UID and SECRET

Run: python fetch_data_from_censys <date>
Eg: python fetch_data_from_censys 20170207
Date format-> Year+Month+Day

This file fetches the ip+provinces for a particular date and stores in json format
"""
import censys.export
import urllib
import sys
import Config as conf

UID = conf.UID
SECRET = conf.SECRET

c = censys.export.CensysExport(UID, SECRET)
downloads = ['20170426','20170427','20170428','20170429','20170430']
for date_dat in downloads:

	res = c.new_job("select ip, location.latitude, location.longitude from ipv4."+date_dat+" where location.country_code=\"US\" ", "csv", True)
	print res
	job_id = res["job_id"]

	# Wait for job to finish and fetch results
	#print c.check_job_loop(job_id)

	job_loop =  c.check_job_loop(job_id)

	i = 0
	for url in job_loop['download_paths']:
		urllib.urlretrieve(url, 'tmp.csv')
		with open('../data/'+date_dat+'.csv', 'a+') as output, open('tmp.csv','r') as input:
			while True: 
				data = input.read(65536)
				if data:
					output.write(data)
				else:
					break
		print url
		print i
		i = i+1

