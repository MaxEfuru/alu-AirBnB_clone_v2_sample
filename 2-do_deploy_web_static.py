#!/usr/bin/python3
"""Fabric script to distribute an archive to web servers"""

from fabric.api import env, put, run
from os import path

env.hosts = ['<IP web-01>', '<IP web-02>']


def do_deploy(archive_path):
    """Distributes an archive to web servers"""
    if not path.exists(archive_path):
        return False

    try:
        # Upload archive to web server
        put(archive_path, '/tmp/')
        archive_filename = archive_path.split('/')[-1]
        archive_basename = archive_filename.split('.')[0]

        # Create directory to uncompress archive
        run('mkdir -p /data/web_static/releases/{}'.format(archive_basename))

        # Uncompress archive to new directory
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
            .format(archive_filename, archive_basename))

        # Remove archive from web server
        run('rm /tmp/{}'.format(archive_filename))

        # Move contents to new directory and delete old directory
        run('mv /data/web_static/releases/{}/web_static/* \
             /data/web_static/releases/{}/'.format(archive_basename, archive_basename))
        run('rm -rf /data/web_static/releases/{}/web_static'
            .format(archive_basename))

        # Remove old symbolic link and create new one
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
            .format(archive_basename))

        return True

    except:
        return False
