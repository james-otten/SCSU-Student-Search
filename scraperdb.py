########################
# SCSU email scraper db
# James Otten 2014
########################

import sqlite3
import logging

from Objects import *

class ScraperDatabase:
  def __init__(self, db_path='scsuGeo.db'):
    try:
      self.con = sqlite3.connect(db_path)
      self.cur = self.con.cursor()
      self.checkCreateTable()
    except Exception as e:
      logging.error(e)
      print(e)

  def checkCreateTable(self):
    q_person = """CREATE TABLE IF NOT EXISTS t_person(id INTEGER PRIMARY KEY AUTOINCREMENT,
    link TEXT UNIQUE NOT NULL,
    last_name TEXT NOT NULL, 
    first_name TEXT NOT NULL,
    status TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone_id INTEGER,
    local_phone_id INTEGER,
    local_address_id INTEGER,
    perm_address_id INTEGER,
    website_id TEXT)"""
    q_phone = """CREATE TABLE IF NOT EXISTS t_phone(id INTEGER PRIMARY KEY,
    phone TEXT UNIQUE NOT NULL)"""
    q_address = """CREATE TABLE IF NOT EXISTS t_address(id INTEGER PRIMARY KEY,
    address TEXT UNIQUE NOT NULL,
    lat TEXT,
    long TEXT)"""
    q_website = """CREATE TABLE IF NOT EXISTS t_website(id INTEGER PRIMARY KEY,
    website TEXT UNIQUE NOT NULL)"""
    try:
      self.cur.execute(q_person)
      self.cur.execute(q_phone)
      self.cur.execute(q_address)
      self.cur.execute(q_website)
    except Exception as e:
      logging.error(e)
      print(e)
    
  def insertPerson(self, link, last, first, status, email, phone):
    #TODO: SQL injection
    try:
      phone_id = 0
      if phone != None:
        q_phone = """INSERT OR IGNORE INTO t_phone (phone) VALUES("%s")""" % phone
        self.cur.execute(q_phone)
        phone_id = int(self.cur.lastrowid)
      else:
        phone_id = 'null'
      query = """INSERT OR IGNORE INTO t_person """
      query += """(link, last_name, first_name, status, email, phone_id) VALUES("""
      query += """"%s","%s","%s","%s","%s",%s)""" % (str(link), str(last), str(first), str(status), str(email), str(phone_id))
      self.cur.execute(query)
      self.con.commit()
    except Exception as e:
      logging.error(e)
      print(e)
  
  def insert_single(self, table, column, value):
    col_id = 0
    try:
      value = value.strip()
      if table != '' and column != '' and value != '':
        query = """INSERT OR IGNORE INTO %s (%s) VALUES("%s")""" % (table, column, value)
        self.cur.execute(query)
        self.con.commit()
        self.cur.execute("""SELECT id FROM %s WHERE %s="%s" """%(table, column, value))
        row = self.cur.fetchall()
        if len(row) == 1:
          col_id = int(row[0][0])
    except Exception as e:
      logging.error(e)
      print(e)
    finally:  
      return col_id
  
  #TODO Exceptions
  def add_more(self, link, local, perm, website, local_phone):
    print(link)
    local_id = self.insert_single('t_address', 'address', local)
    perm_id = self.insert_single('t_address', 'address', perm)
    web_id = self.insert_single('t_website', 'website', website)
    local_phone_id = self.insert_single('t_phone', 'phone', local_phone)
    q_update = """UPDATE t_person SET """
    if (local_id + perm_id + web_id + local_phone_id) > 0:
      if local_id > 0:
        q_update += """local_address_id = %s,""" % local_id
      if perm_id > 0:
        q_update += """ perm_address_id = %s,""" % perm_id
      if web_id > 0:
        q_update += """ website_id = %s,""" % web_id
      if local_phone_id > 0:
        q_update += """ local_phone_id = %s""" % local_phone_id
      if q_update[-1] == ',':
        q_update = q_update[:-1]
      q_update += """ WHERE link="%s" """ % link
      self.cur.execute(q_update)
      self.con.commit()

  def get_urls(self, count=0, offset=0):
    try:
      q_select = ''
      if count == offset and count == 0:
        q_select = """SELECT link FROM t_person"""
      else:
        q_select = """SELECT link FROM t_person LIMIT %d, %d""" % (offset, count)
      self.cur.execute(q_select)
      return self.cur.fetchall()
    except Exception as e:
      logging.error(e)
      print(e)
    return None
  
  def get_empty_addresses(self, count=0, offset=0):
    try:
      q_select = ''
      if count == offset and count == 0:
        q_select = """SELECT id,address FROM t_address WHERE lat is null OR long is null"""
      else:
        q_select = """SELECT id,address FROM t_address WHERE lat is null OR long is null LIMIT %d, %d""" % (offset, count)
      self.cur.execute(q_select)
      return self.cur.fetchall()
    except Exception as e:
      logging.error(e)
      print(e)
    return None
  
  def get_addresses(self, count=0, offset=0):
    try:
      q_select = ''
      if count == offset and count == 0:
        q_select = """SELECT * FROM t_address WHERE lat is not null AND long is not null"""
      else:
        q_select = """SELECT * FROM t_address WHERE lat is not null AND long is not null LIMIT %d, %d""" % (offset, count)
      self.cur.execute(q_select)
      return self.cur.fetchall()
    except Exception as e:
      logging.error(e)
      print(e)
    return None

  def add_geolocation(self, address_id, lat, lon, formatted_address):
    try:
      if address_id != None and lat != None and lon != None:
        q_select = """SELECT id FROM t_address WHERE address="%s" """ % (formatted_address)
        self.cur.execute(q_select)
        rows = self.cur.fetchall()
        for row in rows:
          self.cur.execute("""UPDATE t_person SET local_address_id="%s" WHERE local_address_id="%s" """ % (row[0], address_id))
          self.cur.execute("""DELETE FROM t_address WHERE id=%s""" % address_id)
        else:
          q_update = """UPDATE t_address SET lat="%s",long="%s", address="%s" WHERE id=%s""" % (lat, lon, formatted_address, address_id)
        self.cur.execute(q_update)
        self.con.commit()
    except Exception as e:
      logging.error(e)
      print(e)

  def get_year(self, year):
    try:
      if len(year) != 2 or int(year) < 0:
        raise Exception('Argument out of range: %s' % year)
      q_year = """SELECT * FROM t_person WHERE email LIKE '%%%s%%'""" % year
      self.cur.execute(q_year)
      people = []
      rows = self.cur.fetchall()
      return rows
    except Exception as e:
      logging.error(e)
      print(e)
      return None
      
  def fetchall(self):
    query = """SELECT COUNT(*) FROM t_person"""
    self.cur.execute(query)
    print(self.cur.fetchall()[0])
    
  def getall(self):
    ret = []
    query = """SELECT * FROM t_person"""
    self.cur.execute(query)
    rows = self.cur.fetchall()
    for row in rows:
      print(row)
      payload = {'LocLat':'0', 'LocLon':'0', 'PermLat':'0', 'PermLon':'0', 'FirstName':row[3], 'LastName':row[2], 'Email':row[5]}
      if row[6] != None: #phone
        q_perm = """SELECT * FROM t_phone WHERE id=%d""" % row[6]
        self.cur.execute(q_perm)
        phone = self.cur.fetchall()
        if len(phone) > 0:
          payload['Phone'] = phone[0][1]
      if row[8] != None:#LocalAddress
        q_perm = """SELECT * FROM t_address WHERE id=%d""" % row[8]
        self.cur.execute(q_perm)
        address = self.cur.fetchall()
        if len(address) > 0:
          payload['LocalAddress'] = address[0][1]
          if address[0][2] != None:
            payload['LocalLat'] = address[0][2]
            payload['LocalLon'] = address[0][3]
      if row[9] != None: #PermAddress
        q_perm = """SELECT * FROM t_address WHERE id=%s""" % row[9]
        self.cur.execute(q_perm)
        address = self.cur.fetchall()
        if len(address) > 0:
          payload['PermAddress'] = address[0][1]
          if address[0][2] != None:
            payload['PermLat'] = address[0][2]
            payload['PermLon'] = address[0][3]
      if row[10] != None: #Website
        q_perm = """SELECT * FROM t_website WHERE id=%s""" % row[10]
        self.cur.execute(q_perm)
        site = self.cur.fetchall()
        if len(site) > 0:
          payload['Website'] = site[0][1]
      #print(payload)
      ret.append(payload)
    return ret
