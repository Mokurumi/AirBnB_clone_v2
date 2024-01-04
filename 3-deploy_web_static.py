#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web servers
"""
from fabric.api import *
from os import path
from datetime import datetime


env.hosts = ['100.27.2.172', '100.25.158.175']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


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
    if not path.exists(archive_path):
        return False
    try:
        put(archive_path, "/tmp/")
        file_name = archive_path.split('/')[1].split('.')[0]
        run("sudo mkdir -p /data/web_static/releases/{}/".format(file_name))
        run("sudo tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/"
            .format(file_name, file_name))
        run("sudo rm /tmp/{}.tgz".format(file_name))
        run("sudo mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/".format(file_name, file_name))
        run("sudo rm -rf /data/web_static/releases/{}/web_static"
            .format(file_name))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(file_name))
        return True
    except:
        return False
    
def deploy():
    """
    Creates and distributes an archive to your web servers
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
