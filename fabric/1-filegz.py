# coding=utf-8

from fabric.api import *
from fabric.contrib.files import exists

env.user = 'python'
env.hosts = ['192.168.31.72']
env.password = 'liubojun'

@task
@runs_once
def tar_task():
    with lcd('/home/python/Desktop'):
        local('tar -zcvf te.tar.gz test')

@task
def put_task():
    if not exists('/home/python/Desktop/demo', use_sudo=True):
        sudo('mkdir -p /home/python/Desktop/demo')
    with cd('/home/python/Desktop/demo'):
        put('/home/python/Desktop/te.tar.gz','/home/python/Desktop/demo/de.tar.gz',use_sudo=True)

@task
def check_task():
    lmd5 = local('md5sum /home/python/Desktop/te.tar.gz',capture=True).split(' ')[0]
    rmd5 = run('md5sum /home/python/Desktop/demo/de.tar.gz').split(' ')[0]
    if lmd5==rmd5:
        print('file is completed:ok...')
    else:
        print('file is not right,is error...')

@task
def run_task():
    with cd('/home/python/Desktop/demo'):
        sudo('tar -zxvf de.tar.gz')
        with cd('test'):
            sudo('python 1.py')
@task
def go():
    tar_task()
    put_task()
    check_task()
    run_task()


