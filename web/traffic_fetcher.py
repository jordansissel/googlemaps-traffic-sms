#!/usr/local/bin/python

import cgi
import popen2
import os
import miscdb
from email.MIMEImage import MIMEImage
import smtplib
import time
import urllib

def check_whitelist(request):
  (user,domain) = request["replyto"].split("@")
  ret = False
  ret = ret or (user == "4089315410")
  ret = ret or ("csh.rit.edu" in domain)
  return ret

def fetch_image(request):
  cmd = "/u9/psionic/projects/traffic/traffic.sh"
  url = "http://www.semicomplete.com/projects/traffic/app/test.html"
  url = "%s?%s" % (url, urllib.urlencode(request))
  (proc_out, proc_in) = popen2.popen2([cmd, url])
  traffic_image = proc_out.read().split("\n")[0]
  print "image: %s" % traffic_image
  proc_out.close()
  proc_in.close()
  return traffic_image

def mail_image(filename, request):
  fd = open(filename, "rb")
  image_data = fd.read()
  fd.close()

  msg = MIMEImage(image_data)
  msg['Subject'] = 'Traffic for "%s"' % request["q"]
  msg['To'] = request["replyto"]
  msg['From'] = "psionic+traffic@csh.rit.edu"

  s = smtplib.SMTP()
  s.connect()
  s.sendmail(msg['From'], [msg['To']], msg.as_string())
  s.close()

  os.unlink(traffic_image)

  print "Content-type: text/plain"
  print

  print "OK"

form = cgi.FieldStorage()
while True:
  db = miscdb.RecDB("/u9/psionic/s/projects/traffic/app/requests.db")
  db.Open(create_if_necessary=True)

  queue = []
  #print "%f: start loop" % time.time()
  for i in db.ItemIterator():
    print "Found: %s" % i
    queue.append(i)

  for i in queue:
    if not check_whitelist(i.value):
      print "Skipping request not in whitelist: %s" % i.value
      continue
    print "Processing: %s" % i.value
    traffic_image = fetch_image(i.value)
    mail_image(traffic_image, i.value)
    db.Delete(i.row, i.timestamp)
  db.Close()
  time.sleep(1)
