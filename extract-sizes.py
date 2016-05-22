#!/usr/bin/python
#
# Determine the sizes of a bunch of images.
#
# Usage:
# ./extract-sizes.py '*.jpg' > sizes.txt
#
# Produces a CSV file with three columns:
# file-basename-no-extension,width,height

import glob
import os.path
import re
import subprocess
import sys
import record
import fetcher

#for pattern in sys.argv[1:]:
#  for path in glob.glob(pattern):
#    size_str = subprocess.check_output(['identify', path])

#    m = re.search(r' (\d+)x(\d+) ', size_str)
#    assert m, size_str
#    width, height = [int(x) for x in m.groups()]
#    assert width > 0
#    assert height > 0

#    base, _ = os.path.splitext(os.path.basename(path))

#    print '%s,%d,%d' % (base, width, height)

#Funziona similmente a thumbnailer

rs = record.AllRecords()
f = fetcher.Fetcher('images', 0)
rs = [r for r in rs if (r.photo_url and f.InCache(r.photo_url))]
for idx, r in enumerate(rs):
  in_image = f.CacheFile(r.photo_url)
  size_str = subprocess.check_output(['identify', f.CacheFile(r.photo_url)])

  m = re.search(r' (\d+)x(\d+) ', size_str)
  assert m, size_str
  width, height = [int(x) for x in m.groups()]
  assert width > 0
  assert height > 0

  base = r.photo_id()

  print '%s,%d,%d' % (base, width, height)
