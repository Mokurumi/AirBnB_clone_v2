#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers
"""
from fabric.api import env, put, run, local
from os.path import exists
from datetime import datetime
env.hosts = ['100.27.2.172', '100.25.158.175']
env.user = 'ubuntu'


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    """
    try:
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        local("mkdir -p versions")
        file_name = "versions/web_static_{}.tgz".format(current_time)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception as e:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if exists(archive_path):
        archived_file = archive_path.split("/")[1]
        filename_no_ext = archived_file.split(".")[0]
        arc_file_remote = "/tmp/{}".format(archived_file)
        new_version = "/data/web_static/releases/{}/".format(filename_no_ext)
        put(archive_path, arc_file_remote)
        run("mkdir -p {}".format(new_version))
        run("tar -xzf {} -C {}".format(arc_file_remote, new_version))
        run("rm {}".format(arc_file_remote))
        run("mv -f {}web_static/* {}".format(new_version, new_version))
        run("rm -rf {}web_static".format(new_version))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(new_version))
        print("New version deployed!")
        return True
    else:
        return False
