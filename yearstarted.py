#!/usr/bin/python3
########################
# SCSU email scraper year started school
# James Otten 2014
########################

import sys
import re

from scraperdb import ScraperDatabase

def main():
  year = '12'
  args = sys.argv
  if len(args) == 2:
    year = args[1]
  db = ScraperDatabase()
  try:
    rows = db.get_year(year)
  except Exeption as e:
    print(e)
  pat = re.compile('[a-zA-Z]{4}%s[0-9]{2}@stcloudstate\.edu' % year)
  for row in rows:
    if re.match(pat, row[5]) != None:
      print(row[5])

if __name__ == '__main__': main()
