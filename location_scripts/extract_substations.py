import shapefile
import csv
from sets import Set 

#Investiages if all points on line implied substations
#Just end points => 55,210 points
#Including all points => 2121955
#US has ~55k substations so just go with end points
#Verifably correct?

#Read in all transmission lines
print("Loading shapefile")
sf = shapefile.Reader("trans_ln/trans_ln.shp")
# shapes = sf.shapes()

substations = set()

shapeRecs = sf.shapeRecords()

total_points = 0 

print("Iterating over shapes")
for shape in shapeRecs:
  points = shape.shape.points
  num_points = len(points)
  total_points += num_points

  for i, point in enumerate(points):
    if i is 0 or i is num_points - 1:
      substations.add((point[1], point[0]))

subwriter = csv.writer(open("endpoints.csv", 'w'))

print("Writing to file")
for sub in list(substations):
  subwriter.writerow(sub)

print("Average points per line = " + str(float(total_points / len(shapeRecs))))