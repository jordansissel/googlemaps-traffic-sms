#!/usr/local/bin/python

import sys
import cgi
import miscdb

form = cgi.FieldStorage()

db = miscdb.RecDB("/u9/psionic/s/projects/traffic/app/requests.db")
db.Open(create_if_necessary=True)

print "Content-type: text/plain"
print

data = {}
for i in form.keys():
  data[i] = form.getvalue(i)

for i in ("q", "replyto"):
  if i not in data:
    print "No %r specified" % i
    sys.exit(1)

db.Set("request", data)
db.Close()
