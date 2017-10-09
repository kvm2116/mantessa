import sys
import csv
import operator

try:
	successIPsReader = csv.reader(open(sys.argv[1], 'rb'))
	successIPsSorted = sorted(successIPsReader, key=operator.itemgetter(0))
except:
	print "no file name inputed"
	exit()

try:
	ipScoresReader = csv.reader(open('ipscores.csv', 'rb'))
	ipScoresSorted = sorted(ipScoresReader, key=operator.itemgetter(0))
except:
	ipScoresSorted = []

# print "opened files"

s = 0
c = 0
newSuccessIPs = []
currIPs = []

while s < len(successIPsSorted) and c < len(ipScoresSorted):
	success = successIPsSorted[s][0]
	curr, score_str, total_str = ipScoresSorted[c][0:3]
	score = float(score_str)
	total = float(total_str)
	
	'''
	due to current set up of zmap (to only return successful pings)
	if on first ping, ip is not up, the ip is instantly rotated out 
	this means all additions, start at 1/1 scoring
	'''
	if success < curr:
		newSuccessIPs.append([success, 1, 1, 1])
		s += 1
	elif success == curr:
		score += 1
		total += 1.0
		currIPs.append([curr, score, total, score/total])
		s += 1
		c += 1
	else:
		total += 1.0
		currIPs.append([curr, score, total, score/total])
		c += 1

# print "overlap complete"

while s < len(successIPsSorted):
	success = successIPsSorted[s][0]
	newSuccessIPs.append([success, 1, 1, 1])
	s += 1

# print "appended new successful"

while c < len(ipScoresSorted):
	curr, score_str, total_str = ipScoresSorted[c][0:3]
	score = float(score_str)
	total = float(total_str) + 1.0
	currIPs.append([curr, score, total, score/total])
	c += 1

currIPs.sort(key = lambda row: row[3])
swapped_count = 0
i = 0

print "popped IPs:"
while swapped_count < int(0.1*len(currIPs)) and i < len(currIPs):
	if currIPs[i][2] >= 5 and currIPs[i][3] <= 0.6:
		poppedIP = currIPs.pop(i)
		print poppedIP[0], poppedIP[3]
		swapped_count += 1
	else:
		i += 1

# print currIPs

# print ipScoresSorted
# print "ip scores\n-----------------"
# print currIPs
# print "curr ips list\n-----------------"
# print newSuccessIPs
# print "new ips list\n-----------------"

ipScoresWriter = csv.writer(open('ipscores.csv', 'wb'))

for ip in newSuccessIPs:
	ipScoresWriter.writerow(ip)

for ip in currIPs:
	ipScoresWriter.writerow(ip)

print sys.argv[1], "complete"
print