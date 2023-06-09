#! /usr/bin/env python
# Authors:
#   Sotirios Roussis <root@xtonousou.com>

import os
import time
import logging

import dotenv
import requests
import docker

from providers import dockerhub
from notifications import *


config = {**dotenv.dotenv_values("./dup.env"), **dotenv.dotenv_values("./dup.creds.env"), }

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


class Docker(object):

    def __init__(self):
        self.session = requests.Session()
        self.client = docker.from_env()
        self.registries = {
            "dockerhub": dockerhub.Provider(self.session, config["DUP_DOCKERHUB_ACCESS_TOKEN"]),
        }

    def get_images(self):
        images = {}

        # iterate running containers
        for c in self.client.containers.list(all=False):
            docker_image_id = c.image.short_id.split(":")[-1]

            docker_container_image_repo_tags = c.image.attrs.get("RepoTags")
            docker_image_name, docker_image_tag = "", ""
            if docker_container_image_repo_tags:
                docker_image_name, docker_image_tag = docker_container_image_repo_tags[0].split(":")

            docker_image = f"{docker_image_name}:{docker_image_tag}" if docker_image_name else None
            if not docker_image:
                logging.warning(f"container: {c.name} | skipping locally built image")
                continue

            logging.info(f"container: {c.name} | image: {docker_image}")

            if not docker_image in images.keys():
                images[docker_image] = {
                    "id": c.image.attrs.get("Id").strip(),
                    "name": docker_image_name,
                    "tag": docker_image_tag,
                    "containers": [c.name, ],
                }
                continue

            images[docker_image]["containers"].append(c.name)

        return images

    def check_images(self, images):
        for ik, iv in images.items():
            for rk, rv in self.registries.items():
                self.registries[rk].compare_image(iv)
                logging.info(f"registry: {rk} | image: {ik}")

    def main(self):
        images = self.get_images()
        self.check_images(images)


if __name__ == "__main__":
    d = Docker()

    while True:
        d.main()
        time.sleep(int(config["DUP_CHECK_INTERVAL"].strip()))
