import csv
import operator
from dateutil.parser import parse

try:
	fplReader = csv.reader(open('fpl.csv', 'rb'))
	fplData = sorted(fplReader, key=operator.itemgetter(0))
	# filteredReader = csv.reader(open('filtered.csv', 'rb'))
	# filteredData = sorted(fplReader, key=operator.itemgetter(0))
except:
	exit()

try:
	optimalReader = csv.reader(open('optimal.csv', 'rb'))
	optimalData = sorted(optimalReader, key=operator.itemgetter(0))
except:
	print("optimal open failed")
	exit()


i = 0
j = 0

while i < len(fplData):
	fpldate = parse(fplData[i][0])
	smallest_diff = abs((fpldate - parse(optimalData[j][0])).total_seconds())
	smallest_found = False
	j += 1

	while not smallest_found:
		diff = abs((fpldate - parse(optimalData[j][0])).total_seconds())
		if diff > smallest_diff:
			smallest_found = true
			print(fplData[i][0] + " " + optimalData[j-1][0] + " " + smallest_diff)
		else:
			smallest_diff = diff
			j += 1
	i += 1
