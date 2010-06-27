# DEPLOYMENT PROCESS

# Create tempory folder to copy files needed for install
# Setup config file appropriately for deployment
# create package of files
# Move file to server
# unpack files on server

# Does any cleanup of server need to be done?

from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ['server2']

#def test():
#    with settings(warn_only=True):
#        result = local('./manage.py test my_app', capture=False)
#    if result.failed and not confirm("Tests failed. Continue anyway?"):
#        abort("Aborting at user request.")

def clean():
    """Cleans temporary area for deployment"""
    local('rm -rf /tmp/icanhelp')
    
def copy():
    """Copies files for deployment to temp folder and sets configs for 
    deployment."""
    local('cp -r . /tmp/icanhelp')
    local('rm /tmp/icanhelp/config.py')
    local('''echo "URL_BASE=r'/icanhelp/'" > /tmp/icanhelp/config.py''')
    
def pack():
    """Build package file for deployment"""
    with cd('/tmp'):
        local('find icanhelp -name "*pyc" | xargs rm')
        local('tar czf /tmp/icanhelp.tgz icanhelp', capture=False)

def prepare():
    clean()
    copy()
    pack()

def deploy():
    put('/tmp/icanhelp.tgz', '/tmp/')
    with cd('~/www/'):
        run('tar xzf /tmp/icanhelp.tgz')
        run('chmod 775 icanhelp')
    with cd('~/www/icanhelp/'):
        run('touch code.py')
        run('chmod 660 db.sqlite')
        run('chmod 770 sessions')

def clean_server():
    with cd('~/www/'):
        run('rm -rf icanhelp')

