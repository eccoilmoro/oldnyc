./facebook_fetcher.py
cd nyc
./csv-to-record-facebook.py
cd ..
./generate-geocodes.py --coders ravenna_coder --pickle_path nyc/records.pickle --output_format locations.txt --geocode -n > locations.txt
./cluster-locations.py locations.txt > lat-lon-map.txt
./generate-geocodes.py --coders ravenna_coder --pickle_path nyc/records.pickle --lat_lon_map lat-lon-map.txt --output_format lat-lons-ny.js --geocode > viewer/static/js/nyc-lat-lons-ny.js
cp ./nyc/records.pickle records.pickle
./image_fetcher.py -n 12000
./image_thumbnailer.py
./extract-sizes.py  > nyc-image-sizes.txt
rm records.pickle
cd nyc
./generate_popular.py
./generate_fb_links.py
cd ..
cd ../oldnyc.github.io
git add .
git commit -m 'photo update'
cd ../oldnyc
./generate_static_site.py
cp ./thumbnails/* ../oldnyc.github.io/thumb/
cp ./viewer/static/js/* ../oldnyc.github.io/js/
cd ../oldnyc.github.io/
./update-js-bundle.sh
sudo systemctl start apache2.service

