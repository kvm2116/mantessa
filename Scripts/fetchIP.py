"""
This is a python script to fetch all the IP addresses for a network using censys.io API

NOTE: To view functions for a package, use the pydoc command in the terminal. For instance "pydoc censys" or "pydoc censys.ipv4"

Author: Kunal Mahajan
		(mkunal@cs.columbia.edu)
"""

import argparse
import censys.ipv4
import csv

parser = argparse.ArgumentParser("Fetch IP addresses from Censys.io")
parser.add_argument('uid', help='Censys UID')
parser.add_argument('secret', help='Censys SECRET')
parser.add_argument('netaddr', help='Network address to search')
parser.add_argument('outfile', help='File to store the output')

args = parser.parse_args()
UID = args.uid
SECRET = args.secret
netaddr = args.netaddr
out_filename = args.outfile

def getips():
	ipv4s = censys.ipv4.CensysIPv4(UID, SECRET)
	# fields = ["parsed.subject_dn", "parsed.fingerprint_sha256", "parsed.fingerprint_sha1"]

	writer = csv.writer(open(out_filename, 'w'))
	for c in ipv4s.search(netaddr):
		writer.writerow([c['ip']])

getips()