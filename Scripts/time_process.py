import csv
import operator
from datetime import datetime

try:
	whitelistIPsReader = csv.reader(open('whitelistfraction.csv', 'rb'))
	whitelistIPsSorted = sorted(whitelistIPsReader, key=operator.itemgetter(0))
except:
	whitelistIPsSorted = []

try:
	whitelistIPsWriter = csv.writer(open('whitelistfraction2.csv', 'ab'))
except:
	exit()

i = 0

#./irma_data9.9-18/20170909T17_00_34Z.csv
#'20170915', '21_00_34'
while i < len(whitelistIPsSorted):
	datetime_split = whitelistIPsSorted[i][0].split('/')[2].replace('Z', 'T').split('T')[0:2]
	year = int(datetime_split[0][0:4])
	month = int(datetime_split[0][4:6])
	day = int(datetime_split[0][6:])
	time_split = datetime_split[1].split('_')
	hour = int(time_split[0])
	minute = int(time_split[1])
	second = int(time_split[2])
	time = datetime(year, month, day, hour, minute, second)
	row = [time, whitelistIPsSorted[i][1]]
	print row
	whitelistIPsWriter.writerow(row)
	i += 1
