#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers
"""
from fabric.api import *
from os.path import exists


env.hosts = ['100.27.2.172', '100.25.158.175']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if exists(archive_path) is False:
        return False
    try:
        put(archive_path, "/tmp/")
        file_name = archive_path.split("/")[-1]
        path_no_ext = "/data/web_static/releases/{}".format(
            file_name.split(".")[0])
        run("mkdir -p {}".format(path_no_ext))
        run("tar -xzf /tmp/{} -C {}".format(file_name, path_no_ext))
        run("rm /tmp/{}".format(file_name))
        run("mv {}/web_static/* {}/".format(path_no_ext, path_no_ext))
        run("rm -rf {}/web_static".format(path_no_ext))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(path_no_ext))
        return True
    except:
        return False
