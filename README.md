SCSU-Student-Search
===================

Scripts for analyzing data scraped from the SCSU student directory.

Data only shown for students whose last name begins with the letter O. 

Please contact me for more information about the entire data set.

Check out my [ASP.NET MVC 5 web application](http://scsusearch.azurewebsites.net/) using the same data set.

Scripts:
--------
distance.py - Finds the distance between a students address and the SCSU campus.

geo.py - Geolocation using Google Maps API. Add your API key to the config to use.

yearstarted.py - Detects the year the student first registered with SCSU.

Library:
--------
scraperdb.py - SQLite database connection.

Objects.py - Self rolled classes for ORM.

Other:
------
SCSUStudentSearch.cfg - Configuration, add Google Maps API key here.

scsuGeo.db - SQLite database.
