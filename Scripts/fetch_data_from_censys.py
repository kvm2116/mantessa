"""
Author: tusharag171@gmail.com/ta2482@columbia.edu
Co-Author: nb2776@columbia.edu

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
date_dat = sys.argv[1]
# Start new Job
res = c.new_job("select ip,location.province from ipv4."+date_dat+" where location.registered_country_code=\"US\" LIMIT 5")
print res
job_id = res["job_id"]

# Wait for job to finish and fetch results
#print c.check_job_loop(job_id)

job_loop =  c.check_job_loop(job_id)

url = job_loop['download_paths'][0]

"""
f1 = open(date_dat+'.txt', 'w+')
f1.write(job_loop['download_paths'][0])
f1.write("\n")
f1.close()
"""

urllib.urlretrieve(url, date_dat+'.json')