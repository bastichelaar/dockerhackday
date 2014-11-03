#!/usr/bin/env python
import sys
import json
import base64
from docker import Client

c = Client(base_url='unix://var/run/docker.sock')


def stop_containers(containers):
    for container in containers:
        c.stop(container)
        c.remove_container(container)
        print "Removed container with id %s" % container


def start_container(image, tag):
    # TODO command should not be "/bin/sleep" but the original command
    container = c.create_container(image + ":" + tag, command="/bin/sleep 3000")
    containerid = container.get('Id')
    c.start(container=containerid, publish_all_ports=True)
    print "Started container %s from image %s:%s" % (containerid, image, tag)


def start_containers(image, tag, nr):
    for i in range(nr):
        id = start_container(image, tag)


def find_containers_to_replace(name, excluded_id):
    # TODO Should this find stopped containers as well?
    containers_to_replace = []
    up_to_date = 0
    for container in c.containers():
        if container["Image"].split(":")[0] == name:
            if c.inspect_container(container["Id"])["Image"] != excluded_id:
                containers_to_replace.append(container["Id"])
            else:
                up_to_date += 1
    return containers_to_replace, up_to_date


def find_image_id(repository, tag):
    # TODO It might be possible to filter the combination of repo:tag directly
    # https://docs.docker.com/reference/api/docker_remote_api_v1.15/#22-images
    repotag_to_find = u"%s:%s" % (repository, tag)
    for image in c.images(repository):
        if repotag_to_find in image["RepoTags"]:
            return image["Id"]


def pull_image(image, tag):
    print "Pulling image %s:%s" % (image, tag)
    response = c.pull(image, tag=tag)


for line in sys.stdin:
    try:
        message = json.loads(line)
    except:
        continue

    if message:
        for image in message:
            imagejson = json.loads(base64.b64decode(image["Payload"]))
            image = imagejson["image"]
            tag = imagejson["tag"]
            print "The %s:%s image has been updated, starting update of running containers" % (image, tag)

            pull_image(image, tag)
            id_to_deploy = find_image_id(image, tag)

            if id_to_deploy == None:
                print "Image %s:%s could not be pulled, exiting" % (image, tag)
                sys.exit(1)

            print "Pulled image %s:%s with id %s" % (image, tag, id_to_deploy)

            containers_to_replace, up_to_date = find_containers_to_replace(image, id_to_deploy)
            print "There are %d container(s) to replace, %d already up to date" % (len(containers_to_replace), up_to_date)

            if len(containers_to_replace) == 0:
                print "Nothing to replace, exiting"
                sys.exit(0)

            start_containers(image, tag, len(containers_to_replace))

            stop_containers(containers_to_replace)

            print "Done"
