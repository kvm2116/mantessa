import csv
import random
fileName = "ips.tsv"

def populateGrid():
	grid = {}
	with open(fileName) as tsvfile:
		reader = csv.reader(tsvfile,delimiter='\t')
		for row in reader:
			long = row[1]
			lat = row[2]
			gridPosition = assignGrid(long, lat)
			if gridPosition in grid:
				grid[gridPosition].append(row)
			else:
				grid[gridPosition] = [row]
	return grid

def generateWhiteList(grid, n)
	wList{}
	for key, value in grid:
		wList[key] = random.sample(value, 2)

		


