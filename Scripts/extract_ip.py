"""
Author: tusharag171@gmail.com/ta2482@columbia.edu

This files extracts the IP address and the corresponding states from the input
json file and stores it into a text file.
"""

import json
import sys

with open('81c116eb-bd8c-445c-aaa6-ff5acd6b3aab-000000000000.json') as f:
	sys.stdout = open('output.txt', 'w')
	for line in f:
		print json.loads(line)['ip'] +' '+json.loads(line)['location']['province']
	sys.stdout.close()



