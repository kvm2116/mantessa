import csv
import sys 

data = {}

with open(sys.argv[1], 'r') as sr, open(sys.argv[2], 'w+') as dest:
  reader = csv.reader(sr)
  writer = csv.writer(dest)
  writer.writerow(["lng", "lat"])

  for d in reader:
    if (d[1], d[0]) in data:
      data[(d[1], d[0])] += 1
    else:
      data[(d[1], d[0])] = 1

  counts = list(data.values())

  norm = [float(i)/max(counts) * 10000 for i in counts]
  keys = list(data.keys())

  for i, key in enumerate(keys):
    for j in range(0, int(norm[i])):
      writer.writerow((key[1], key[0]))


