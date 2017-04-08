# import  gmplot
import csv
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

lats = []
longs = []

#Run with python3 map_ips.py <csv of ips> <offset of ip lat in csv> 

with open(sys.argv[1], 'r') as f:
	reader = csv.reader(f, delimiter=',', quotechar='|')
	for line in reader:
		lats.append(float(line[int(sys.argv[2]) + 0]))
		longs.append(float(line[int(sys.argv[2]) + 1]))

fig = plt.figure()

themap = Basemap(projection='gall',
              llcrnrlon = -126,             
              llcrnrlat = 18,               
              urcrnrlon = -60,               
              urcrnrlat = 53,               
              resolution = 'l',
              area_thresh = 100000.0,
              )

themap.drawcoastlines()
themap.drawcountries()
themap.fillcontinents(color = 'gainsboro')
themap.drawmapboundary(fill_color='steelblue')

x, y = themap(longs, lats)
themap.plot(x, y, 
            'o',                    
            color='Indigo',         
            markersize=1            
            )

plt.show()