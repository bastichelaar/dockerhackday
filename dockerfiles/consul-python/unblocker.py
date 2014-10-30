#!/usr/bin/env python

import sys
import json
import base64
import docker

for line in sys.stdin:
    print line
    try:
        message = json.loads(line)
    except:
        continue

    if message:
        print base64.b64decode(message["Value"])
