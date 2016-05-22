#!/usr/bin/env python
'''Generates popular-photos.js.

Data source is facebook-posts.csv Ho modificato completamente la logica di questo programma. 
'''

import csv
import sys
import json

def run():
    

    photos = []
    id_to_photo = {}

    fields = ['fb_id', 'fb_message',  'fb_likes',  'fb_shares', 'fb_create_time',  'fb_object_id',  'fb_status_type',  'fb_full_picture', 'fb_link', 'Description', 'Year',  'Credits']
    reader = csv.DictReader(file('../facebook-posts.csv'),fields,delimiter=';')


    for row in reader:
        if row['fb_object_id'] == '':
            break
        if row['fb_shares'] < 110:
            break
        photo = {
            'id': row['fb_object_id'],
            'date': row['Year'],
            'loc': 'Ravenna',
            'desc': row['Description'].replace("<br/>"," ")
        }
        photos.append(photo)
        id_to_photo[photo['id']] = photo

    sys.stderr.write('Loaded %d popular images\n' % len(photos))

    for row in csv.reader(open('nyc-image-sizes.txt')):
        photo_id, width, height = row
        width = int(width)
        height = int(height)
        try:
            id_to_photo[photo_id]['height'] = int(round(200. * height/width))
        except KeyError:
            pass

    for row in photos:
        assert 'height' in row

    open('viewer/static/js/popular-photos.js', 'w').write(
            'var popular_photos = %s;\n' % json.dumps(photos))

if __name__ == '__main__':
    run()
