#!/usr/bin/python
#
# Run whatever's in the "location" field directly through the geocoder.


import fileinput
import re
import sys
import json
import csv
#import nyc.boroughs

if __name__ == '__main__':
  sys.path += (sys.path[0] + '/..')

import coders.registration
import record


#boros = '(?:Cervia|Borgo San Biagio|Borgo S.Biagio|Borgo San Rocco|Borgo S.Rocco|Bosco Baronio|Marina di Ravenna|Punta Marina|Classe|)'
#boros_re = r'(?:Cervia|Borgo San Biagio|Borgo S.Biagio|Borgo San Rocco|Borgo S.Rocco|Bosco Baronio|Marina di Ravenna|Punta Marina|Classe|)'

streets = '(?:Vicolo|Strada|Viale|Piazza|Vicolo|Casa|Piazzale|Via|Rotonda|Porta|Via Ponte|Via Porta)'

# example: "100th Street (East) & 1st Avenue, Manhattan, NY"
# 30337 / 36328 (0.8351)
#cross_and_re = r'(.*) (?:&|and|at) (.*), (%s)' % boros

# example: "38th Street (West) - Twelfth Avenue, Manhattan, NY"
#  1616 / 36328 (0.0445)
#cross_dash_re = r'([^-,]*?) - ([^-,]*?)(?:[-,].*)?, (%s)' % boros

# example: "York Avenue #1646-50 - 87th Street looking southeast, Manhattan, NY"
#   225
#address1_re = r'(.*? %s) #([0-9]+).*(%s)' % (streets, boros)

# example: "929 Park Avenue. Near Eighty-first Street., Manhattan, NY"
#   313
#address2_re = r'(\d+)(?:-\d+)? ([a-zA-Z 0-9]*? %s).*, (%s)' % (streets, boros)

#address3_re = r'((%s\s+(San|S.|Santi|Santissimo|Santissima)\s+[A-Z]{1}[a-z]+ |%s\s+[a-z]+\s+[A-Z]{1}[a-z]+ |%s\s+[A-Z]{1}[a-z]+))' % (streets,streets,streets)

#

address3_re = ur'(?:Via Porta|Vicolo|Strada|Viale|Piazza|Vicolo|Casa|Piazzale|Via|Rotonda|Porta|Chiesa di|Basilica di)\s+(?:San|S.|Santi|Santissimo|Santissima|XX|IV)\s+[A-Z]{1}[a-z]+|(?:Via Ponte|Via Porta|Vicolo|Strada|Viale|Piazza|Vicolo|Casa|Piazzale|Via|Rotonda|Porta|Mausoleo|Palazzo|Circonvallazione|Battistero|Molo|Canale)\s+[a-zA-Z]+\s+[A-Z]{1}[a-z]+|(?:Via Ponte|Via Porta|Piazza Anita|Piazza Dora|Piazza Andrea|Vicolo|Strada|Viale|Piazza|Vicolo|Casa|Piazzale|Via|Rotonda|Porta|Ponte|Giardini|giardini|Porto|Darsena|S.|San|Santa|Sant.|Biblioteca|Loggetta|Bagno|Villaggio|Torre|Pialassa|Molo|Hotel|Circolo|Battistero|Teatro|Canale)\s+[A-Z]{1}[a-z]+|(?:Darsena|darsena|[S,s]tazione|[I,i]ppodromo|Mirabilandia|Standiana|Bassette|Liceo Classico|Candiano|Baretto|Mercato Coperto|Anic|Sarom|Portonaccio|Pala de Andr.|colonia|Colonia|S.Apollinare|Duomo|Diga|Capanno Garibaldi|Rocca Brancaleone|Piazza dell.Aquila|Sant.Apollinare|[O,o]spedale|[f,F]aro|Tomba di Dante|Stadio|S Giovanni Evangelista|[p,P]alazzo di Teodorico)'

city_re = ur'(?:Marina di Ravenna|Punta Marina|Cervia|Milano Marittima|Classe|Lido Adriano|Casal Borsetti|Casalborsetti|Marina Romea|Porto Corsini|Lido di Savio|Lido di Dante|Fosso Ghiaia|Coccolia)'

#address4_re = r'((%s .* ))' % (boros)

#cross_patterns = [cross_and_re, cross_dash_re]
addr_patterns = [address3_re]

city_patterns = [city_re]

# (From Wikipedia)
#staten_neighborhoods = r'Annadale|Arden Heights|Arlington|Arrochar|Bay Terrace|Bloomfield|Brighton Heights|Bulls Head|Castleton|Castleton Corners|Charleston|Chelsea|Clifton|Concord|Dongan Hills|Egbertville|Elm Park|Eltingville|Emerson Hill|Fort Wadsworth|Graniteville|Grant City|Grasmere|Great Kills|Greenridge|Grymes Hill|Hamilton Park|Heartland Village|Huguenot|Lighthouse Hill|Livingston|Manor Heights|Mariners Harbor|Mariner\'s Harbor|Meiers Corners|Midland Beach|New Brighton|New Dorp|New Springville|Oakwood|Ocean Breeze|Old Place|Old Town|Pleasant Plains|Port Richmond|Prince\'s Bay|Randall Manor|Richmond Valley|Richmondtown|Rosebank|Rossville|Sandy Ground|Shore Acres|Silver Lake|South Beach|St\. George|Stapleton|Stapleton Heights|Sunnyside|Todt Hill|Tompkinsville|Tottenville|Tottenville Beach|Travis|Ward Hill|Westerleigh|West New Brighton|Willowbrook|Woodrow'

# def RemoveStatenIslandNeighborhood(addr):
#   if 'Staten Island' in addr:
#     addr = re.sub(staten_neighborhoods_re, ', ', addr)
#   return addr


# Should "Island" be included in this?
#place_suffixes = r'Park|Bridge|Campus|College|Station|Church|Square|Hotel|Cemetery|Hospital|Beach|University|Building|Point|H\.S\.|School'

# example: "Empire State Building, Manhattan, N.Y."
# 1083
#place_re = r'(.*? (?:%s))\.?, ((?:(?:%s), )?%s)' % (place_suffixes, staten_neighborhoods, boros)

# example: "P.S. 5., Brooklyn, N.Y." (-> Should come out as "PS 123")
# ~150
#ps_re = '((?:PS|P\.S\.|Public School) (?:#|No\. )?\d+\.?), ((?:(?:%s), )?%s)' % (staten_neighborhoods, boros)
#place_patterns = [place_re, ps_re]

#ps_cleanup_re = r'(?:PS|P\.S\.|Public School) (?:#|No\. )?(\d+)\.?'


class RavennaCoder:
  def __init__(self):
    pass

  def codeRecord(self, r):
    #if r.source() != 'Milstein Division': return None

    #loc = self._extractLocationStringFromRecord(r)
    loc = r.location().strip()
    m = None
    
    

   
    

    #determine the city
    for pattern in city_patterns:
        #sys.stderr.write("0-City:" + loc+" ")
        #m = re.match(pattern, loc)
        p = re.compile(pattern)
        m = re.search(p, loc)
        if m: break
    if m:
      city=m.group(0)+',Italy'
    else:
      city='Ravenna,Italy'


    #search first in well_known_locations.csv
    fields = ['location', 'exclusion', 'Address']
    reader = csv.DictReader(file('./coders/well_known_locations.csv'),fields,delimiter=';')
    next(reader) #skip header
    exact_address = ''
    for idx, row in enumerate(reader):

      if row['location'].lower() in loc.lower() and  ( row['exclusion'].strip() == ''  or (row['exclusion'].strip() <> '' and (row['exclusion'].strip().lower() + ' ' ) not in loc.lower())):
        exact_address = row['Address']
        sys.stderr.write('WELL KNOWN LOCATIONS-Resp : Trovata la via ESATTA! %s' % exact_address)
        break
    if exact_address.strip() <> '' :
      return {
          #'address': '%s %s, %s' % (number, street, city),
          'address' : '%s, %s' % (exact_address, city),  
          'source': loc,
          'type': 'street_address'
        }



    #search second in ravenna_geocode_helper.csv
    fields = ['fb_id', 'fb_message',  'fb_likes',  'fb_shares', 'fb_create_time',  'fb_object_id',  'fb_status_type',  'fb_full_picture', 'fb_link', 'Description', 'Year',  'Credits', 'Address']
    reader = csv.DictReader(file('./coders/ravenna_geocode_helper.csv'),fields,delimiter=';')
    next(reader) #skip header
    exact_address = ''
    for idx, row in enumerate(reader):
      if row['fb_object_id'] == r.photo_id() :
        exact_address = row['Address']
        sys.stderr.write('0000000000000000000-Resp : Trovata la via ESATTA! %s' % exact_address)
        break
    if exact_address.strip() <> '' :
      return {
          #'address': '%s %s, %s' % (number, street, city),
          'address' : '%s, %s' % (exact_address, city),  
          'source': loc,
          'type': 'street_address'
        }

    m = None

    for pattern in addr_patterns:
      sys.stderr.write("1-Loc:" + loc+" ")

      p = re.compile(pattern)
      m = re.search(p, loc)

      #m = re.match(pattern, loc)
      if m: break
    if m:
      sys.stderr.write('2-Resp : Trovata la via! ')
      #number, street, city = m.groups()
      #sys.stderr.write('3-Trovato ' + m.group(0) + ' \n')
      street = m.group(0)
    
      # number & street may be swapped.
      #try:
      #  x = int(number)
      #except ValueError:
      #  number, street = street, number
      
      return {
          #'address': '%s %s, %s' % (number, street, city),
          'address' : '%s, %s' % (street, city),  
          'source': loc,
          'type': 'street_address'
        }
    else:
       sys.stderr.write('2-Resp : NON Trovata la via ; %s; %s; %s \n' % (r.photo_id(),city, loc))

       #geocodes just the city
       return {
          #'address': '%s %s, %s' % (number, street, city),
          'address' : '%s, %s' % ('', city),  
          'source': loc,
          'type': 'street_address'
       }

    sys.stderr.write('(%s) Bad location: %s\n' % (r.photo_id(), loc));
    return None


  #def _extractLocationStringFromRecord(self, r):
  #  raw_loc = r.location().strip()
  #  loc = re.sub(r'^[ ?\t"\[]+|[ ?\t"\]]+$', '', raw_loc)
  #  return loc


  def _getLatLonFromGeocode(self, geocode, data):
    for result in geocode['results']:
      # partial matches tend to be inaccurate.
      # if result.get('partial_match'): continue
      # data['type'] is something like 'address' or 'intersection'.
      #if data['type'] in result['types']:
        loc = result['geometry']['location']
        return (loc['lat'], loc['lng'])


  #def _getBoroughFromAddress(self, address):
  #  m = re.search(boros_re, address)
  #  assert m, 'Failed to find borough in "%s"' % address
  #  record_boro = m.group(1)
  #  if record_boro == 'New York':
  #    record_boro = 'Manhattan'
  #  return record_boro


  def getLatLonFromGeocode(self, geocode, data, r):
    '''Extract (lat, lon) from a Google Maps API response. None = failure.
    
    This ensures that the geocode is in the correct borough. This helps catch
    errors involving identically-named crosstreets in multiple boroughs.
    '''
    latlon = self._getLatLonFromGeocode(geocode, data)
    if not latlon:
      return None
    lat, lon = latlon

    #geocode_boro = nyc.boroughs.PointToBorough(lat, lon)
    #record_boro = self._getBoroughFromAddress(data['address'])

    #if geocode_boro != record_boro:
    #  sys.stderr.write('Borough mismatch: "%s" (%s) geocoded to %s\n' % (
    #      self._extractLocationStringFromRecord(r), record_boro, geocode_boro))
    #  return None
    
    return (lat, lon)

  def finalize(self):
    pass

  def name(self):
    return 'ravenna_coder'


coders.registration.registerCoderClass(RavennaCoder)


# For fast iteration
if __name__ == '__main__':
  coder = RavennaCoder()
  r = record.Record()
  num_ok, num_bad = 0, 0
  for line in fileinput.input():
    addr = line.strip()
    if not addr: continue
    r.tabular = {
      'i': ['PHOTO_ID'],
      'l': [addr],
      'a': ['Milstein Division']
    }
    result = coder.codeRecord(r)

    print '"%s" -> %s' % (addr, result)
    if result:
      num_ok += 1
    else:
      num_bad += 1

  sys.stderr.write('Parsed %d / %d = %.4f records\n' % (
    num_ok, num_ok + num_bad, 1. * num_ok / (num_ok + num_bad)))
