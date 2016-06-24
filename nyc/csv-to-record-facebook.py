#!/usr/bin/python
#
# Converts the milstein.csv file to a pickle file of Record objects.
# NOTE! Should be run from the nyc directory.

import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir) 

import cPickle
import record
import csv

output_file = "records.pickle"
f = file(output_file, "w")
p = cPickle.Pickler(f, 2)

fields = ['fb_id', 'fb_message',  'fb_likes',  'fb_shares', 'fb_create_time',  'fb_object_id',  'fb_status_type',  'fb_full_picture', 'fb_link', 'Description', 'Year',  'Credits']
reader = csv.DictReader(file('../facebook-posts.csv'),fields,delimiter=';')
next(reader) #skip header
try:
  
  for idx, row in enumerate(reader):

    url = str(row['fb_link'])
    assert url

    img_url = str(row['fb_full_picture'])
    assert img_url

    photo_id = str(row['fb_object_id'])
    assert photo_id

    date_str = str(row['Year'])
    # date_str is not always present

    full_address = str(row['Description'].replace(".",""))
    creator = str(row['Credits'])

    title = str(row['Description'])
    assert title

    # TODO(danvk): move this into record.py
    r = record.Record()
    r.thumbnail_url = img_url  # TODO(danvk): real thumbnail
    r.photo_url = img_url
    r.preferred_url = url
    r.tabular = {
      'l': [full_address],  # NOTE: "Location" = folder for SFPL, not address
      'i': [photo_id],
      'p': [date_str],
      'r': [''],  # description
      't': [title],
      'n': [''],  # notes
      'a': ['C era una volta Ravenna']
    }
    p.dump(r)

    print r.thumbnail_url
    count = 1 + idx
    if count % 100 == 0:
      print "Pickled %d records" % count

except Exception, e:
  print e
