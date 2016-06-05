#!/usr/bin/env python
'''Generates fb_links.js.

Data source is facebook-posts.csv . 
'''

import csv
import sys
import json

def run():
    

    photos = []
    id_to_photo = {}

    fields = ['fb_id', 'fb_message',  'fb_likes',  'fb_shares', 'fb_create_time',  'fb_object_id',  'fb_status_type',  'fb_full_picture', 'fb_link', 'Description', 'Year',  'Credits']
    reader = csv.DictReader(file('../facebook-posts.csv'),fields,delimiter=';')
    next(reader) #skip header

    for row in reader:
        photo = {
            'id': row['fb_object_id'],
            'fb_url': row['fb_link']
        }
        photos.append(photo)
        id_to_photo[photo['id']] = photo

    sys.stderr.write('Loaded %d images fb_link \n' % len(photos))

    open('../viewer/static/js/fb_links.js', 'w+').write(
            'var fb_links = %s;\n' % json.dumps(photos))

if __name__ == '__main__':
    run()
