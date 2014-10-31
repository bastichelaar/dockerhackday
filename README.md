dockerhackday
=============

- First pull the requested image
- Loop over the images to get the image's id (this could be parsed from the pull response in step 1)
- Find container ids of containers with the same image name
- Start containers with the new image
- Stop the containers that were old

Test with:

```
fig up
docker run -d ubuntu:14.04 sleep 3000000 && docker run -d ubuntu:14.10 sleep 3000000
consul event -http-addr boot2docker:8500 -name newimage '{"image":"ubuntu", "tag":"14.04"}'
consul event -http-addr boot2docker:8500 -name newimage '{"image":"ubuntu", "tag":"14.10"}'
```
