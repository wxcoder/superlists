from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

"""
Fabric Script for Deployment
"""

REPO_URL = 'https://github.com/wxcoder/superlists.git'

def deploy():
    """
        env.host address of server specified at cmd line
        env.user username to log in to the server
    """
    site_folder ='/home/%s/sites/%s' %(env.user, env.host)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)

def _create_directory_structure_if_necessary(site_folder):
    """
        run runs the shell cmd on the server.
        Create directories if necessary
    """
    for subfolder in ('database', 'static','virtualenv','source'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))

def _get_latest_source(source_folder):
    """
        Look for the .git hidden folder to check whether the repo has 
        already been cloned in that folder. Capture output from git log
        invocation to get the hash of the current commit that's in your 
        local tree. Server will end up with whatever is is on your machine
        that has been pushed to the server. At the end, blow away current
        changes in the server's code directory.
    """
    if exists(source_folder + '/.git/'):
        run('cd %s && git fetch' % (source_folder,)) #pull down latest commits
    else:
        run('git clone %s %s' % (REPO_URL, source_folder)) #bring down a fresh source tree
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('cd %s && git reset --hard %s' % (source_folder, current_commit)) 

def _update_settings(source_folder, site_name):
    """
        Fabric sed cmd does string substituion in a file
        Django uses SECRET_KEY for some of its crypto-cookues and CSFR protection
        code will generate a new key if there isn't one already.
    """
    settings_path = source_folder +'/superlists/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["%s"]' % (site_name,))
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv(source_folder):
    """
     Look for pip executable inside virtual env folder and
     use pip install -r to install requirements
    """ 
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python=python3 %s' %(virtualenv_folder,))
    run('%s/bin/pip install -r %s/requirements.txt' % (
            virtualenv_folder, source_folder
    ))

def _update_static_files(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput' % ( # 1
        source_folder,
    ))

def _update_database(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py migrate --noinput' % (
        source_folder,
    ))
