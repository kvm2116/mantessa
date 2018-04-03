startLat = 25.118
startLon = -124.733056
latIncrement = 0.159
lonIncrement= 0.220

def assignGrid(lat, lon):
	difLat = lat - startLat
	difLon = lon - startLon
	xCoord = difLat/latIncrement
	yCoord = difLon/lonIncrement
	print("xCoord: {}".format(int(xCoord)))
	print("yCoord: {}".format(int(yCoord)))


assignGrid(33, -90.74)
