#!/usr/bin/env python

import email.Parser
import sys
import re
import urllib

p = email.Parser.Parser()
msg = p.parse(sys.stdin)

m = re.search("[^< ]+@[^ >]+", msg.get("From"))
if not m:
  sys.exit(0)

sender = m.group(0)

(user, domain) = sender.split("@")

mms_map = {
  "txt.att.net": "mms.att.net"
};

domain = mms_map.get(domain, domain)
replyto = "%s@%s" % (user, domain)

base_url = "http://www.semicomplete.com/projects/traffic/app/send_request"
query = [x.strip() for x in msg.get_payload().split("\n") if x.strip()][0]

data = {
  "q": query,
  "replyto": sender,
}

url = "%s?%s" % (base_url, urllib.urlencode(data))
print url
