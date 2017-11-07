import sys
import csv
import operator

'''
reads csvs to fill in newCurrIPs and newSuccessIPs lists with IPs with updated scores
sorts newCurrIPs with smallest scores at the top
'''
def score_update(alpha, successIPsSorted, currIPsSorted, newCurrIPs, newSuccessIPs):
	#s, c iterators for successIPSorted and currIPsSorted respectively
	s = 0
	c = 0
	
	#iterates through overlap area of successIPsSorted and currIPsSorted
	while s < len(successIPsSorted) and c < len(currIPsSorted):
		success = successIPsSorted[s][0]
		curr, total_str, score_str = currIPsSorted[c]
		total = float(total_str)
		score = float(score_str)
		
		'''
		due to current set up of zmap (to only return successful pings)
		if on first ping, ip is not up, the ip is instantly rotated out 
		this means all additions, start at 1/1 scoring
		'''
		if success < curr:
			newSuccessIPs.append([success, 1, 1])
			s += 1
		elif success == curr:
			new_score = (1 - alpha) * score + alpha * 1
			total += 1
			newCurrIPs.append([curr, total, new_score])
			s += 1
			c += 1
		else:
			new_score = (1 - alpha) * score + alpha * 0
			total += 1
			newCurrIPs.append([curr, total, new_score])
			c += 1

	#adding in additional successful IPs
	while s < len(successIPsSorted):
		success = successIPsSorted[s][0]
		newSuccessIPs.append([success, 1, 1])
		s += 1

	
	#updating scores for additional existing IPs
	while c < len(currIPsSorted):
		curr, total_str, score_str = currIPsSorted[c]
		total = float(total_str)
		score = float(score_str)

		new_score = (1 - alpha) * score + alpha * 0
		total += 1
		newCurrIPs.append([curr, total, new_score])
		c += 1

	#sort by score (curr: percentage success)	
	newCurrIPs.sort(key = lambda row: row[2])


'''
pop out IPs according to param values
'''
def popIPs(swap_rate, min_perc, min_hit, newCurrIPs):
	swapped_count = 0
	i = 0
	print "popped IPs:"
	while swapped_count < int(swap_rate*len(newCurrIPs)) and i < len(newCurrIPs):
		if newCurrIPs[i][1] >= min_hit and newCurrIPs[i][2] <= min_perc:
			poppedIP = newCurrIPs.pop(i)
			print poppedIP[0], poppedIP[2]
			swapped_count += 1
		else:
			i += 1
	print "total popped:", swapped_count
	newCurrIPs.sort(key = lambda row: (row[2], row[1]), reverse=True)


def main():
	alpha = 0.125
	swap_rate = 0.1
	min_perc = 0.7
	min_hit = 10

	#opening and sorting corresponding csvs
	try:
		successIPsReader = csv.reader(open(sys.argv[1], 'rb'))
		successIPsSorted = sorted(successIPsReader, key=operator.itemgetter(0))
	except:
		print "no file name inputed"
		exit()

	try:
		ipScoresReader = csv.reader(open('ipscores.csv', 'rb'))
		currIPsSorted = sorted(ipScoresReader, key=operator.itemgetter(0))
	except:
		currIPsSorted = []

	newCurrIPs = []
	newSuccessIPs = []

	score_update(alpha, successIPsSorted, currIPsSorted, newCurrIPs, newSuccessIPs)
	popIPs(swap_rate, min_perc, min_hit, newCurrIPs)

	# try:
	# 	valRemovedWriter = csv.writer(open('valsremoved.csv', 'wb'))
	# except:
	# 	print "swap count not saved"

	# valRemovedWriter = csv.writer(open('valsremoved.csv', 'ab'))
	# removed = [sys.argv[1], swapped_count]
	# valRemovedWriter.writerow(removed)


	#wipe old file and write in new values
	open("ipscores.csv", "w").close()
	ipScoresWriter = csv.writer(open('ipscores.csv', 'wb'))

	for ip in newCurrIPs:
		ipScoresWriter.writerow(ip)

	for ip in newSuccessIPs:
		ipScoresWriter.writerow(ip)

	print sys.argv[1], "complete"
	print


main()