#Alexander Kutner ak3987
#prompts user for directory of files to process into .csv

import os
import json
import csv
import glob

directory_in_str="/local/mantessa/irma-data/fpl-data/*"

def isolateJSON(st):
	start = "define("
	end = ");"
	startCut=len(start)
	st=st[0]
	st=st[startCut:]
	st=st.replace(end,"")
	return st


writeTo=open('flpa-irma-data.csv','w')
writer = csv.writer(writeTo, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
for filename in glob.glob(directory_in_str):
	try:
		with open(filename) as data:
			js = data.readlines()
		if len(js)>0:
			js=isolateJSON(js)
			parsed_json=json.loads(js)
			counties=parsed_json['counties']
			timestamp=parsed_json['lastupdated']
			for county in counties:
				writer.writerow([counties[county]['name'],timestamp,str(counties[county]['numberofoutages']),str(counties[county]['numberofaccounts'])])
	except :
		print(filename+" not accessed")

writeTo.close()

print("flpa-irene-data.csv written to current directory")
