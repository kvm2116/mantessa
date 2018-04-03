import json

startLat = 25.118
startLon = -124.733056
currentLat = startLat
currentLon = startLon
latIncrement = 0.159
lonIncrement= 0.220
maxLat = 49.002
maxLong = -66.947028
latCounter = 0
lonCounter = 0

geoObject = {}
geoObject['type'] = "FeatureCollection"
features = []
while(currentLat <= maxLat):
	while (currentLon <= maxLong):
		featureObject = {
			"type": "Feature",
			"geometry": {
				"type": "Polygon",
				"coordinates": [
					[
						[currentLat, currentLon],
						[currentLat +latIncrement, currentLon],
						[currentLat, currentLon + lonIncrement],
						[currentLat + latIncrement, currentLon + lonIncrement]
					]
				]
			},
			"properties": {
				"name": "[{},{}]".format(latCounter, lonCounter)
			}
		}
		features.append(featureObject)
		currentLon += lonIncrement
		lonCounter += 1
	currentLon = startLon
	lonCounter = 0
	currentLat += latIncrement
	latCounter += 1
geoObject['features'] = features
jsonString = json.dumps(geoObject)
print jsonString

