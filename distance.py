#!/usr/bin/python3
########################
# Calculate distance of addresses from SCSU
# James Otten 2014
########################

import math

from scraperdb import ScraperDatabase

#SCSU campus
LAT = 45.5480263
LON = -94.1509631

def degree_to_radian(deg):
  return deg * (math.pi/180)

def km_to_mi(km):
  return km * 0.621371192

def distance(lat1, lon1, lat2, lon2):
  R = 6371
  deltaLat = degree_to_radian(lat2 - lat1)
  deltaLon = degree_to_radian(lon2 - lon1)
  a = (math.sin(deltaLat/2) * math.sin(deltaLat/2)) 
  a += math.cos(degree_to_radian(lat1)) * math.cos(degree_to_radian(lat2)) * math.sin(deltaLon/2) * math.sin(deltaLon/2)
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
  d = R * c
  return km_to_mi(d)

db = ScraperDatabase()
rows = db.get_addresses()
for row in rows:
  lat = float(row[2])
  lon = float(row[3])
  print('%s {%f, %f}: %f' % (row[1].replace('\n',', '), lat, lon, distance(LAT, LON, lat, lon)))
  