import sys
import csv
import operator

def time_convert(name):
	datetime_split = name[0].split('/')[2].replace('Z', 'T').split('T')[0:2]
	year = int(datetime_split[0][0:4])
	month = int(datetime_split[0][4:6])
	day = int(datetime_split[0][6:])
	time_split = datetime_split[1].split('_')
	hour = int(time_split[0])
	minute = int(time_split[1])
	second = int(time_split[2])
	time = datetime(year, month, day, hour, minute, second)
	return time


def count_hits(successIPsSorted, whitelistIPsSorted):
	s = 0
	c = 0
	up = 0
	#can be static based on whitelist size
	total = 0

	#iterates through overlap area of successIPsSorted and whitelistIPsSorted
	while s < len(successIPsSorted) and c < len(whitelistIPsSorted):
		success = successIPsSorted[s][0]
		curr = whitelistIPsSorted[c][0]

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
	while c < len(whitelistIPsSorted):
		total += 1
		c += 1

	return up*1.0/total


def main():
	#opening and sorting corresponding csvs
	try:
		successIPsReader = csv.reader(open(sys.argv[1], 'rb'))
		successIPsSorted = sorted(successIPsReader, key=operator.itemgetter(0))
	except:
		print "no file name inputed"
		exit()

	try:
		whitelistIPsReader = csv.reader(open('ipscores.csv', 'rb'))
		whitelistIPsSorted = sorted(whitelistIPsReader, key=operator.itemgetter(0))
	except:
		whitelistIPsSorted = []

	fraction_up = count_hits(successIPsSorted, whitelistIPsSorted)

	fractionUpWriter = csv.writer(open('whitelistfraction.csv', 'ab'))
	time = time_convert(sys.argv[1])
	row = [time, fraction_up]
	fractionUpWriter.writerow(row)
	print row


main()