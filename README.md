# dockerhackday

- First pull the requested image
- Loop over the images to get the image's id (this could be parsed from the pull response in step 1)
- Find container ids of containers with the same image name
- Start containers with the new image
- Stop the containers that were old

Test with:

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
