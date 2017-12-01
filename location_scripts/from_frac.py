import csv
import sys 

data = {}

max = 50

with open(sys.argv[1], 'r') as sr, open(sys.argv[2], 'w+') as dest:
  reader = csv.reader(sr)
  writer = csv.writer(dest)
  writer.writerow(["lng", "lat"])

  for d in reader:
    try:
      llcrnrlon = -124.357662
      llcrnrlat = 32.441678
      urcrnrlon = -113.9917
      urcrnrlat= 41.949 
      
      lon = float(d[1])
      lat = float(d[0])

      if(lon > llcrnrlon and lon < urcrnrlon and lat > llcrnrlat and lat < urcrnrlat):
        if ((float(d[4]) > .5 and float(d[4]) < .9) or  (float(d[4]) > .9 and int(d[3]) > 1000)): #If lat long of interest
          data[(d[1], d[0])] = float(d[2]) * max
    except:
      pass

  counts = list(data.values())
  # print(counts)
  keys = list(data.keys())
  data.clear()
  for i, key in enumerate(keys):
      print("coords: " + str(key[1]) + "," + str(key[0]) + " count:" + str(counts[i]))
      #for j in range(0, int(counts[i])):
        #writer.writerow((key[0], key[1]))
