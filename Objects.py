########################
# Person and Address objects
# James Otten 2014
########################

class Serializable:
  def __str__(self):
    raise NotImplementedError()
  def json(self):
    raise NotImplementedError()
  def csv(self):
    raise NotImplementedError()
  def xml(self):
    raise NotImplementedError()

class Address:
  def __init__(self, address, lat, lon):
    self.address = address
    self.lat = lat
    self.lon = lon
    
  def __str__(self):
    ret = self.address
    if self.lat != None and self.lon != None:
      ret += ' {%s, %s}' % (self.lat, self.lon)
    return ret

class Person:
  def __init__(self, idNum, link, last_name, first_name, status, email, phone, local_phone, local_address, perm_address, website):
    self.idNum = idNum
    self.link = link
    self.last_name = last_name
    self.first_name = first_name
    self.status = status
    self.email = email
    self.phone = phone
    self.local_phone = local_phone
    self.local_address = local_address
    self.perm_address = perm_address
    self.website = website
    
  def __init__(self, rows):
    if len(rows) != 11:
      print(rows)
      raise Exception('Invalid row data')
    self.idNum = rows[0]
    self.link = rows[1]
    self.last_name = rows[2]
    self.first_name = rows[3]
    self.status = rows[4]
    self.email = rows[5]
    #Optional fields
    self.phone = None
    self.local_phone = None
    self.local_address = None
    self.perm_address = None
    self.website = None
    print(row[6])
    if row[6] != None and row[6] != 'null':
      self.phone = row[6]
    if row[7] != None and row[7] != 'null':
      self.local_phone = row[7]
    if row[8] != None and row[8] != 'null':
      self.local_address = row[8]
    if row[9] != None and row[9] != 'null':
      self.perm_address = row[9]
    if row[10] != None and row[10] != 'null':
      self.website = row[10]
    
  def __str__(self):
    ret = '%s %s, %s %s' % (self.idNum, self.last_name, self.first_name, self.email)
    if self.phone != None:
      ret += ' %s' % self.phone
    if self.local_phone != None:
      ret += ' %s' % self.local_phone
    if self.local_address != None:
      ret += ' %s' % self.local_address
    if self.perm_address != None:
      ret += ' %s' % self.perm_address
    if self.website != None:
      ret += ' %s' % self.website
    return ret
