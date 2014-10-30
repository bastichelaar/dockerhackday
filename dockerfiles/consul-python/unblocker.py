#!/usr/bin/env python

import sys
import json
import base64
from docker import Client

c = Client(base_url='unix://var/run/docker.sock')


def stop_containers(image):
    for container in c.containers():
        if container["Image"].split(":")[0] == image:
            response = c.stop(container["Id"])
            print response


def create_container(image):
    container = c.create_container(image["name"] + ":" + str(image["version"]), command='/bin/sleep 30')
    response = c.start(container=container.get('Id'))
    print response
    


for line in sys.stdin:
    print line
    try:
        message = json.loads(line)
    except:
        continue

    if message:
        for image in message:
            imagejson = json.loads(base64.b64decode(image["Payload"]))
            #print image["Name"] + ":" + base64.b64decode(image["Payload"])
            #create_container(json.loads(base64.b64decode(image["Payload"])))
            stop_containers(imagejson["name"])
