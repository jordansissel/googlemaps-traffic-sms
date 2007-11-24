#!/usr/local/bin/python

import cPickle
import cgi
import urllib

import miscdb

form = cgi.FieldStorage()

KEY = "ABQIAAAA-byvTDSeYW54aJrIuQbYQhTWj7ClNu6S_Uc1hiErWUXlVyZRzRQJiVTg0mYR_sozccMTS5Enytg0Lw"

print "Content-type: text/plain"
print

base_url = "http://maps.google.com/maps/geo"
query = {
  "q": form.getfirst("q"),
  "output": "json",
  "key": KEY,
  "callback": form.getfirst("callback")
}

url = "%s?%s" % (base_url, urllib.urlencode(query))

db = miscdb.RecDB("/u9/psionic/s/projects/traffic/app/geocode.db")
db.Open(create_if_necessary=True)

value = None
try:
  for entry in db.ItemIteratorByRows([url]):
    value = entry.value
    print "//cached"
except miscdb.RowNotFound, e:
  pass

if value is None:
  fd = urllib.urlopen(url)
  value = fd.read()
  db.Set(url, value, 0)

print value

