from geopy.distance import vincenty
import csv
import sys

#Usage: command centers.csv points.csv

substations = {}

with open(sys.argv[1], 'r') as sr, open(sys.argv[2], 'r') as ipr:
  sub_reader = csv.reader(sr)
  print("reading in substations")
  for row in sub_reader:
    substations[(row[0], row[1])] = []

  keys = substations.keys()

  ip_reader = csv.reader(ipr)

  #Compare all ip/ss distances
  print("Doing comparissions")
  for ip in ip_reader:
    minimum = 100000
    min_ss = None
    for ss in keys:
      dist = vincenty((ip[1], ip[2]), ss).miles
      if dist < minimum:
        min_ss = ss
        minimum = dist

    #Save ip to closest substation 
    substations[ss].append(ip)

  #Write dict to file
  output = open('ss_ip_map.csv', 'w')
  w = csv.DictWriter(output, substations.keys())
  w.writerow(substations)
  output.close()
