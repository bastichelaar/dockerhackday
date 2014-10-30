#!/usr/bin/env python

import sys
import json
import base64
from docker import Client

c = Client(base_url='unix://var/run/docker.sock')

for line in sys.stdin:
    print line
    try:
        message = json.loads(line)
    except:
        continue

    if message:
        for image in message:
            #print image["Name"] + ":" + base64.b64decode(image["Payload"])
            imagejson = json.loads(base64.b64decode(image["Payload"]))

            container = c.create_container(imagejson["name"] + ":" + str(imagejson["version"]), command='/bin/sleep 30')
            response = c.start(container=container.get('Id'))
            print response
