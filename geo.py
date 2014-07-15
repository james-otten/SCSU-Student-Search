#!/usr/bin/python3
########################
# SCSU email scraper geolocation via google maps
# James Otten 2014
########################

import requests
from scraperdb import ScraperDatabase
import logging
import configparser
import sys


class Point:
  def __init__(self, lat, lon, formatted):
    self.lat = lat
    self.lon = lon
    self.formatted = formatted

class Geolocation:
  def __init__(self, db, GOOGLE_API_KEY):
    self.db = db
    self.GOOGLE_API_KEY = GOOGLE_API_KEY
  
  def do_lookup(self, count=1):
    rows = self.db.get_empty_addresses(count)
    print(rows)
    for row in rows:
      point = self.get_google_maps(row[1])
      if point != None:
        self.db.add_geolocation(row[0], point.lat, point.lon, point.formatted)
        print('%s -> %s' % (row[1].replace('\n',','), point.formatted))
        print('%s -> lat:%s lon:%s'%(row[1].replace('\n',','), point.lat, point.lon))
      else:
        msg = 'Could not log: %s'%row[0]
        logging.warn(msg)
        print(msg)
  
  def get_google_maps(self, address):
    try:
      url = 'https://maps.googleapis.com/maps/api/geocode/json'
      param={'address':address, 'key':self.GOOGLE_API_KEY}
      req = requests.get(url,params=param)
      json = req.json()
      if json['status'] == 'OK':
        if len(json['results']) != 1:
          logging.warn('Multiple results for: %s'%address)
          return None
        lat = json['results'][0]['geometry']['location']['lat']
        lon = json['results'][0]['geometry']['location']['lng']
        formatted = json['results'][0]['formatted_address']
        if 'partial_match' in json['results'][0].keys() or 'PO BOX' in address.upper():
          formatted = address.replace('\n',', ')
        point = Point(lat, lon, formatted)
        return point
    except Exception as e:
      msg = 'get_google_maps: %s'%str(e)
      logging.error(msg)
      print(msg)
      return None

def main():
  logging.basicConfig(filename='Geo.log', level=logging.DEBUG)
  try:
    count = 10
    if len(sys.argv) == 2:
      val = int(sys.argv[1])
      if val > 0:
        count = val
    config = configparser.RawConfigParser()
    config.read('SCSUStudentSearch.cfg')
    GOOGLE_API_KEY = config.get('gmaps','secret')
    db = ScraperDatabase()
    geo = Geolocation(db, GOOGLE_API_KEY)
    geo.do_lookup(count=10)
  except Exception as e:
    msg = 'External error: %s' % str(e)
    logging.error(msg)
    print(msg)

if __name__ == '__main__': main()
  