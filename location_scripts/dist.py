from geopy.distance import vincenty
import csv
import sys
import time
import math
import pickle
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
  for i, ip in enumerate(ip_reader):
    if i %50000 is 0:
      print ("Processing IP " + str(i))
    minimum = 1000000
    min_ss = None
    # start = time.time()
    for ss in keys:
      dist = vincenty((ip[1], ip[2]), ss).miles #compute true dist
      if dist < minimum:
        min_ss = ss
        minimum = dist
    #Save ip to closest substation 
    substations[min_ss].append(ip)

  #Write dict to file
  # pickle.dump(substations, open("ip_substation_mappings/" + sys.argv[1][:2] + ".pkl", "wb"))
  
  for key in substations.keys():
    print(len(substations[key]))