#!/usr/bin/env python3
"""
Distributes an archive to web servers using the do_deploy function.
"""

import os
from fabric.api import run, put, env

env.hosts = ['<IP web-01>', '<IP web-02>']


def do_deploy(archive_path):
    """
    Distributes an archive to web servers using the do_deploy function.
    """

    # Check if the file exists
    if not os.path.exists(archive_path):
        return False

    # Upload the archive to the /tmp/ directory of the web server
    filename = os.path.basename(archive_path)
    put(archive_path, '/tmp/{}'.format(filename))

    # Uncompress the archive to the folder /data/web_static/releases/<archive filename without extension> on the web server
    directory_name = filename.split('.')[0]
    run('sudo mkdir -p /data/web_static/releases/{}/'.format(directory_name))
    run('sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(filename, directory_name))
    run('sudo rm /tmp/{}'.format(filename))

    # Delete the symbolic link /data/web_static/current from the web server
    run('sudo rm -f /data/web_static/current')

    # Create a new symbolic link linked to the new version of your code (/data/web_static/releases/<archive filename without extension>)
    run('sudo ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(directory_name))

    return True
