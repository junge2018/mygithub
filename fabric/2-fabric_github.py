# coding=utf-8

from fabric.api import *

env.user = 'python'
env.hosts = ['192.168.31.72']
env.password = 'liubojun'

@task
@runs_once
def local_update():
    with lcd('/home/python/Desktop/spider/spider_shell'):
        local('git add -A')
        local('git commit -m "updated"')
        local('git pull study master:master')
        local('git push study master:master')

@task
def remote_update():
    with cd('/home/python/Desktop/django-repo/mygithub'):
        run('git checkout master')
        run('git pull origin master:master')
@task
def func():
    with cd('/home/python/Desktop/django-repo/mygithub'):
        with cd('fabric'):
            run('python test.py')

@task
def deploy():
    print('--start--')
    local_update()
    remote_update()
    func()
    print('--end--')



