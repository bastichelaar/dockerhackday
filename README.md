# Unblocker
Docker Global Hackday #2 project

## What does unblocker do?
The idea is that if you push a new image to a Docker registry, all the running containers with an old version of that image are automatically replaced by the new version.

## How does unblocker work?
Using a [Consul watch](http://www.consul.io/docs/commands/watch.html) we watch the *newimage* event with `unblocker.py` as it's handler. This means that when the *newimage* event is triggered `unblocker.py` gets called with the event's payload as input.

Unblocker then does the following things:
- Pull the new image
- Find containers running an older version of the same image by image repo/name
- Start the same amount of containers with the new image
- Stop the old containers

The end result is that a Docker Registry only has to fire the *newimage* event to automatically update all running containers to the new image :)

## Demo
A live-from-terminal demo can be found here https://asciinema.org/a/13551

To try it yourself use below instructions as a guideline:
```
# Build the consul-python container
docker build -t consul-python dockerfiles/consul-python/
# Start the container
fig up
# Enter the container
docker exec -ti `docker ps -lq` /bin/bash
# Start an ubuntu 14.04 & 14.10 container
docker run -d ubuntu:14.04 sleep 3000 && docker run -d ubuntu:14.10 sleep 3000
# List the currently running containers
docker ps
# Pretend we are are a Docker Registry which has just received an updated image
consul event -http-addr localhost:8500 -name newimage '{"image":"ubuntu", "tag":"14.04"}'
# List the new running containers
docker ps
# Pretend we are are a Docker Registry which has just received an updated image for the second time
consul event -http-addr localhost:8500 -name newimage '{"image":"ubuntu", "tag":"14.10"}'
# List the new running containers
docker ps
```
