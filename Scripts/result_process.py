##################################################################
# Script contains functions for updating watchlist and generating
# scan watchlist. 
# score_update() takes in lists of current IPs and zmap response of  
# successfully pinged IPs to update scores based on exponentially
# weighted moving average and returns value into params
# popIPs() removes IPs based of IP scores and coefficients 
# maintain_watchlist() loads files and runs score_update() 
# and popIPs() to update ipscores.csv
# generate_scan_watchlist() takes ipscores.csv and returns IPs
# above preset min percentage and hits to run outage scans on
# 
# Written by: Chan Pham, tqp2001
##################################################################

import sys
import csv
import operator

'''
Helper function. 
Reads current IP and success IPs to fill in updated_IPs and new_IPs 
with corresponding IPs and updated scores
'''
def score_update(alpha, success_IPs, curr_IPs, updated_IPs, new_IPs):
	#s, c iterators for successIPSorted and curr_IPs respectively
	s = 0
	c = 0
	
	#iterates through overlap area of success_IPs and curr_IPs
	while s < len(success_IPs) and c < len(curr_IPs):
		success = success_IPs[s][0]
		curr, total_str, score_str = curr_IPs[c]
		total = float(total_str)
		score = float(score_str)
		
		'''
		due to current set up of zmap (to only return successful pings)
		if on first ping, ip is not up, the ip is instantly rotated out 
		this means all additions, start at 1/1 scoring
		'''
		if success < curr:
			new_IPs.append([success, 1, 1])
			s += 1
		elif success == curr:
			new_score = (1 - alpha) * score + alpha * 1
			total += 1
			updated_IPs.append([curr, total, new_score])
			s += 1
			c += 1
		else:
			new_score = (1 - alpha) * score + alpha * 0
			total += 1
			updated_IPs.append([curr, total, new_score])
			c += 1

	#adding in additional successful IPs
	while s < len(success_IPs):
		success = success_IPs[s][0]
		new_IPs.append([success, 1, 1])
		s += 1

	
	#updating scores for additional existing IPs
	while c < len(curr_IPs):
		curr, total_str, score_str = curr_IPs[c]
		total = float(total_str)
		score = float(score_str)

		new_score = (1 - alpha) * score + alpha * 0
		total += 1
		updated_IPs.append([curr, total, new_score])
		c += 1

	#sort by score (curr: percentage success)	
	updated_IPs.sort(key = lambda row: row[2])


'''
Helper function. 
Pops out IPs based on coefficients passed in and directly
changes updated_IPs list
swap_rate: max percentage of IPs rotated off
min_score: min score for IP to be rotated off
min_hit: min number of hits for IP to be rotated off
updated_IPs: list of IPs with updated scores
'''
def popIPs(swap_rate, min_score, min_hit, updated_IPs):
	swapped_count = 0
	i = 0
	print "popped IPs:"
	while swapped_count < int(swap_rate*len(updated_IPs)) and i < len(updated_IPs):
		if updated_IPs[i][1] >= min_hit and updated_IPs[i][2] <= min_score:
			poppedIP = updated_IPs.pop(i)
			print poppedIP[0], poppedIP[2]
			swapped_count += 1
		else:
			i += 1
	print "total popped:", swapped_count
	updated_IPs.sort(key = lambda row: (row[2], row[1]), reverse=True)


'''
Updates and returns watchlist csv (ipscores.csv) based on 
coeffs passed to be used for zmap scans
file: zmap returned list of successful IP pings
alpha: alpha value for EWMA score
swap_rate: max percentage of IPs rotated off
min_score: min score for IP to be rotated off
min_hit: min number of hits for IP to be rotated off
updated_IPs: list of IPs with updated scores
'''
def maintain_watchlist(file, alpha, swap_rate, min_score, min_hit):
	#opening and sorting corresponding csvs
	try:
		successIPsReader = csv.reader(open(file, 'rb'))
		success_IPs = sorted(successIPsReader, key=operator.itemgetter(0))
	except:
		print "no file name inputed"
		exit()

	try:
		currIPsReader = csv.reader(open('ipscores.csv', 'rb'))
		curr_IPs = sorted(currIPsReader, key=operator.itemgetter(0))
	except:
		curr_IPs = []

	updated_IPs = []
	new_IPs = []

	score_update(alpha, success_IPs, curr_IPs, updated_IPs, new_IPs)
	popIPs(swap_rate, min_score, min_hit, updated_IPs)

	open("ipscores.csv", "w").close()
	ipScoresWriter = csv.writer(open('ipscores.csv', 'wb'))

	for ip in updated_IPs:
		ipScoresWriter.writerow(ip)

	for ip in new_IPs:
		ipScoresWriter.writerow(ip)


'''
Generates watchlist (ipscan.csv) from general watchlist (ipscores.csv) 
made by generate_watchlist to be used for finding outages
'''
def generate_scan_watchlist(min_score, min_hit):
	try:
		currIPsReader = csv.reader(open('ipscores.csv', 'rb'))
		curr_IPs = sorted(currIPsReader, key=operator.itemgetter(0))
	except:
		print "open of ipscores failed"
		exit()

	try: 
		scanIPsWriter = csv.writer(open("ipscan.csv", "wb"))
	except: 
		print "open ipscan.csv failed"
		exit()

	print("files opened")
	for ip in curr_IPs:
		if ip[1] > min_hit and ip[2] > min_score:
			scanIPsWriter.writerow(ip)	


def main():
	alpha = 0.125
	swap_rate = 0.1
	min_score = 0.8
	min_hit = 50

	# code to maintain_watchlist with each scan
	file = sys.argv[1]
	maintain_watchlist(file, alpha, swap_rate, min_score, min_hit)
	print sys.argv[1], "complete"

	# code to generate scan watchlist for identifying power outages
	generate_scan_watchlist(min_score, min_hit)
	print "ipscan.csv generated"


generate_scan_watchlist(0.8, 50)
print "ipscan.csv generated"
