#!/usr/bin/python3
"""
Write a Fabric script (based on the file 1-pack_web_static.py) that
distributes an archive to your web servers, using the function do_deploy
"""
from fabric.api import *
from os import path
from datetime import datetime


env.hosts = ['100.27.2.172', '100.25.158.175']
env.user = 'ubuntu'


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder
    of your AirBnB Clone repo"""
    try:
        local("mkdir -p versions")
        now = datetime.now()
        date_time = now.strftime("%Y%m%d%H%M%S")
        file_name = "versions/web_static_{}.tgz".format(date_time)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except:
        return None
    
def do_deploy(archive_path):
    """
    Distributes an archive to your web servers, using the function do_deploy
    """
    try:
        if not (path.exists(archive_path)):
            return False

        # upload archive
        put(archive_path, '/tmp/')

        # create target dir
        timestamp = archive_path[-18:-4]
        run('sudo mkdir -p /data/web_static/releases/web_static_{}/'.format(
            timestamp))

        # uncompress archive and delete .tgz
        run('sudo tar -xzf /tmp/web_static_{}.tgz -C\
            /data/web_static/releases/web_static_{}/'
        .format(timestamp, timestamp))

        # remove archive
        run('sudo rm /tmp/web_static_{}.tgz'.format(timestamp))

        # move contents into host web_static
        run('sudo mv /data/web_static/releases/web_static_{}/web_static/*\
            /data/web_static/releases/web_static_{}/'.format(
                timestamp, timestamp))

        # remove extraneous web_static dir
        run('sudo rm -rf /data/web_static/releases/web_static_{}/web_static'
        .format(timestamp))

        # delete pre-existing sym link
        run('sudo rm -rf /data/web_static/current')

        # re-establish symbolic link
        run('sudo ln -s /data/web_static/releases/web_static_{}/\
            /data/web_static/current'.format(timestamp))
    except:
        return False

    # return True on success
    return True
