#!/usr/bin/python3
#Fabric script that generates a .tgz archive from the contents
#of the web_static folder of your AirBnB Clone repo
import os.path
from datetime import datetime
from fabric.api import local


def do_pack():
    """
    generate a .tgz archive from the contents of the web_static folder
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
