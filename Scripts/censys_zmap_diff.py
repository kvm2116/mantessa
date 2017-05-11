"""
This is a python script to compare the list of ip addresses provided by zmap and censys.io.
It stores the diff in a list and writes it to a csv file

Author: Kunal Mahajan
		(mkunal@cs.columbia.edu)
"""

import argparse
import csv

parser = argparse.ArgumentParser(description='Compare list of IP addresses in two csv files')
parser.add_argument('zmap_file', help='zmap file')
parser.add_argument('censys_file', help='censys file')
parser.add_argument('outfile', help='File to store the output')

args = parser.parse_args()
zmap_filename = args.zmap_file
censys_filename = args.censys_file
out_filename = args.outfile

"""
Each row of the output file contains an IP as an element of a list
"""
def saveips(diff_ips, out_filename):
	writer = csv.writer(open(out_filename, 'w'))
	for ip in diff_ips:
		writer.writerow([ip])

def getDiff(zmap_ips, censys_ips):
	diff_ips = {}
	for ip in zmap_ips:
		if ip not in censys_ips and ip not in diff_ips:
			diff_ips[ip] = 1
	diff_size = len(diff_ips)
	print "Number of ZMap IPs NOT in Censys = %d" %(diff_size)

	for ip in censys_ips:
		if ip not in zmap_ips and ip not in diff_ips:
			diff_ips[ip] = 1
	print "Number of Censys IPs NOT in ZMap = %d" %(len(diff_ips) - diff_size)
	return diff_ips

"""
The ip address is stored as a list in the csv file
"""
def read_zmap():
	zmap_ips = {}
	firstline = True
	with open(zmap_filename, 'r') as csvfile:
		zmap_data = csv.reader(csvfile)
		for ip in zmap_data:
			if firstline:
				firstline = False
				continue
			if ip[0] not in zmap_ips:
				zmap_ips[ip[0]] = 1  
	print "ZMap: number of unique ips = %d" %(len(zmap_ips))  
	return zmap_ips

"""
The ip address is stored as a list in the csv file
"""
def read_censys():
	censys_ips = {}
	with open(censys_filename, 'r') as csvfile:
		censys_data = csv.reader(csvfile)
		for ip in censys_data:
			if ip[0] not in censys_ips:
				censys_ips[ip[0]] = 1    
	print "Censys: number of unique ips = %d" %(len(censys_ips))
	return censys_ips

zmap_ips = read_zmap()
censys_ips = read_censys()
diff_ips = getDiff(zmap_ips, censys_ips)
saveips(diff_ips, out_filename)