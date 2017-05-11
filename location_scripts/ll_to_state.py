import stateplane
import csv 
import sys

misses = 0

with open (sys.argv[1], 'r') as coords:
  coord_reader = csv.reader(coords)

  for i, coord in enumerate(coord_reader):
    if i%5000 is 0:
      print("Processing " + str(i))

    try:
      #Get state and first two chars (bc that is state code)
      state = stateplane.identify(float(coord[1]), float(coord[0]), 'short')[:2] 
    except:
      misses += 1
      continue

    state_file = open("substations_states/" + str(state) + "_substations.csv", 'a')
    w = csv.writer(state_file)
    w.writerow(coord)
    state_file.close()