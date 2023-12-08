#!/usr/bin/python3
# This a is a fabric script that deploys archive from web_static folder
from fabric import task, Connection
from os.path import exists


env.hosts = ['100.27.2.172', '100.25.158.175']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """
    Distributes an archive to web servers and performs deployment tasks.

    Args:
        archive_path (str): Path of the archive to be deployed.

    Returns:
        bool: True if all operations are done correctly, otherwise False.
    """
    if not exists(archive_path):
        print(f"Archive '{archive_path}' doesn't exist.")
        return False

    try:
        arch_fname = archive_path.split('/')[-1]
        release_folder = f'/data/web_static/releases/{arch_fname[:-4]}'

        for host in env.hosts:
            with Connection(
                    host,
                    user=env.user,
                    connect_kwargs={"key_filename": env.key_filename}
                    ) as conn:
                # Upload archive to /tmp/ directory on the web server
                conn.put(archive_path, '/tmp/')

                # Uncompress the archive to the releases folder
                conn.sudo(f'mkdir -p {release_folder}')
                conn.sudo(f'tar -xzf /tmp/{arch_fname} -C {release_folder}')
                conn.sudo(f'rm /tmp/{arch_fname}')

                # Delete the existing symbolic link and create a new one
                conn.sudo('rm -f /data/web_static/current')
                conn.sudo(f'ln -s {release_folder} /data/web_static/current')

        return True
    except Exception as e:
        print(f"Error deploying archive: {e}")
        return False
