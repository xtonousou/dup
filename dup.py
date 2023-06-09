#! /usr/bin/env python
# Authors:
#   Sotirios Roussis <root@xtonousou.com>

import os
import logging

import dotenv
import requests
import docker

from notifications import *

config = dotenv.dotenv_values("./dup.env")


def main():
    pass


if __name__ == "__main__":
    main()
