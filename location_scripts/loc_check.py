import math
import csv


li_counter = 0
nyc_counter = 0
mw_counter = 0
error_count = 0

lill_lat = 40.550213
lill_long = -73.746792
liur_lat = 41.163855 
liur_long = -72.244958

nycll_lat = 40.580388
nycll_long = -74.029875 
nycur_lat = 40.845900 
nycur_long = -73.846117

mwll_lat = 34.655030
mwll_long = -105.833270 
mwur_lat = 40.015222
mwur_long = -95.006940

with open ('smost.csv', 'r') as f:
  csv_reader = csv.reader(f, delimiter=',', quotechar='|')

  for row in csv_reader:
    try:
      lat = float(row[1])
      lon = float(row[2])

      if lill_lat < lat and liur_lat < lat and liur_long > lon and lill_long < lon:
        li_counter += 1
      if nycll_lat < lat and nycur_lat < lat and nycur_long > lon and nycll_long < lon:
        nyc_counter += 1
      if mwll_lat < lat and mwur_lat < lat and mwur_long > lon and mwll_long < lon:
        mw_counter += 1
    except: 
      error_count += 1

print(li_counter)
print(nyc_counter)
print(mw_counter)
print(error_count)