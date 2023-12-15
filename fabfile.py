from __future__ import unicode_literals, print_function

import os
import random

from fabric import task
from invocations.console import confirm
from configs import settings

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
VIRTUAL_ENV = os.environ.get('VIRTUAL_ENV') or os.path.join(PROJECT_ROOT, 'env')
VIRTUAL_ENV_ACTIVATE = '. %s' % os.path.join(VIRTUAL_ENV, 'bin/activate')


@task
def runserver(c):
    port = settings.SERVER_PORT
    if not port:
        summ = sum([ord(char) for char in PROJECT_ROOT.split('/')[-1]])
        random.seed(summ)
        port = random.randrange(1024, 5000)

    host_name = '127.0.0.1'
    if os.path.exists('/etc/hosts'):
        with open('/etc/hosts') as f:
            host_name = '%s.local' % settings.SERVER_HOST
            if f.read().find(host_name) != -1:
                host_name = host_name

    with c.prefix(VIRTUAL_ENV_ACTIVATE):
        with c.cd(PROJECT_ROOT):
            c.run(f'uvicorn main:app --reload --host {host_name} --port {port}', pty=True)


@task
def check(c):
    with c.prefix(VIRTUAL_ENV_ACTIVATE):
        c.run('python manage.py check')
        c.run('time flake8 ./core/')


@task
def deploy_local(c, branch=None):
    with c.prefix(VIRTUAL_ENV_ACTIVATE):
        if not branch:
            branch_name = 'main'
        else:
            branch_name = branch

        if not confirm(
                "Are you sure? It will make changes on the remote system and deploy branch: %s" % branch_name):
            c.abort("Ok, aborting launch...")

        c.run('git checkout %s && git pull' % branch_name)
        c.run('pip install -r requirements.txt')
