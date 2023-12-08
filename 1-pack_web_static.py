#!/usr/bin/python3
"""
This a is a fabric script that generates archive from web_static folder
"""


from fabric import task
from datetime import datetime
import os


@task
def do_pack():
    """
    Creates a .tgz archive from the contents of the web_static folder.

    Returns:
        str or None: If the archive is successfully generated, returns the path
        of the created archive. Otherwise, returns None.
    """
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    archive_name = f"web_static_{timestamp}.tgz"
    versions_folder = "versions"

    # Create versions folder if it doesn't exist
    if not os.path.exists(versions_folder):
        os.makedirs(versions_folder)

    try:
        # Create .tgz archive from web_static folder
        with task.local.cwd('web_static'):
            task.local.run(f"tar -cvzf ../{versions_folder}/{archive_name} .")

        # Return path of the created archive
        return f"{os.path.join(versions_folder, archive_name)}"
    except Exception as e:
        print(f"Error packing files: {e}")
        return None
