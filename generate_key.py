#!/usr/bin/env python
#
# Copyright (c) 2017-2022 Wes Moskal-Fitzpatrick
#

# Built-in Modules
import datetime
import base64
import sys
import time
  
 
now = datetime.date.today()
days = 30
future = now + datetime.timedelta(days=days)
expiry = future.timetuple()

timestamp = time.mktime(expiry)

print("Generating key, expiry date: ",future)
secret = [ timestamp, "random_key" ]

b64key= base64.b64encode(str(secret).encode('utf-8'))
key = bytes.decode(b64key)

print("Generated Key: %s\n"%key)
print("Key will expire in %i days."%days)

sys.exit(0)
