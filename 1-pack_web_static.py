#!/usr/bin/python3
# 1. Compress before sending
import os.path
from datetime import datetime
from fabric.api import local


def do_pack():
    """
    generates a .tgz archive from the contents of the web_static
    """
    _date = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(_date.year,
                                                         _date.month,
                                                         _date.day,
                                                         _date.hour,
                                                         _date.minute,
                                                         _date.second)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None
    return file
