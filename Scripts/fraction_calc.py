##################################################################
# Script contains functions for optimal watchlist analysis. 
# frac_calc() is main function that takes in current watchlist
# and a zmap scan result to calculate fraction of optimal
# watchlist up at the time of the zmap scan.
# time_convert() is a function that takes file name and converts
# it out to a datetime value 
# 
# Written by: Chan Pham, tqp2001
##################################################################

import sys
import csv
import operator
from datetime import datetime

'''
Helper function. 
Takes name of zmap scan file and returns time stamp as datetime obj
'''
def time_convert(name):
	print(name)
	datetime_split = name.split('/')[2].replace('Z', 'T').split('T')[0:2]
	year = int(datetime_split[0][0:4])
	month = int(datetime_split[0][4:6])
	day = int(datetime_split[0][6:])
	time_split = datetime_split[1].split('_')
	hour = int(time_split[0])
	minute = int(time_split[1])
	second = int(time_split[2])
	time = datetime(year, month, day, hour, minute, second)
	return time


'''
Returns fraction of optimal list IPs up at time of passed in watchlist
''' 
def frac_calc(watchlist, file):
	s = 0
	c = 0
	up = 0
	#can be static based on whitelist size
	total = 0

	try:
		successIPsReader = csv.reader(open(file, 'rb'))
		successIPsSorted = sorted(successIPsReader, key=operator.itemgetter(0))
	except:
		print "no file name inputed"
		exit()

	try:
		watchlistReader = csv.reader(open(watchlist, 'rb'))
		watchlistSorted = sorted(watchlistReader, key=operator.itemgetter(0))
	except:
		watchlistSorted = []

	#iterates through overlap area of successIPsSorted and whitelistIPsSorted
	while s < len(successIPsSorted) and c < len(watchlistSorted):
		success = successIPsSorted[s][0]
		curr = watchlistSorted[c][0]

		if success < curr:
			s += 1
		elif success == curr:
			up += 1
			total += 1
			s += 1
			c += 1
		else:
			total += 1
			c += 1
	
	#updating scores for additional existing IPs
	while c < len(watchlistSorted):
		total += 1
		c += 1

	fraction_up = up*1.0/total

	fractionUpWriter = csv.writer(open('optimal_frac.csv', 'ab'))
	time = time_convert(file)
	row = [time, fraction_up]
	fractionUpWriter.writerow(row)
	print row, "added to optimal_frac.csv"


# code example for executing fraction_calc
watchlist = sys.argv[1]
file = sys.argv[2]
frac_calc(watchlist, file)
