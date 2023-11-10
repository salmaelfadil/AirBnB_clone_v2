#!/usr/bin/python3
""" deletes out-of-date archives, using the function"""
from fabric.api import *


env.hosts = ['54.145.85.75', '100.25.145.243']
env.user = "ubuntu"


def do_clean(number=0):
    """ deletes out-of-date archives"""

    number = int(number)

    if number == 0:
        number = 2
    else:
        number += 1

    local('cd versions ; ls -t | tail -n +{} | xargs rm -rf'.format(number))
    path = '/data/web_static/releases'
    run('cd {} ; ls -t | tail -n +{} | xargs rm -rf'.format(path, number))
