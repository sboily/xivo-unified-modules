# -*- coding: utf-8 -*-

# Copyright (C) 2013 Sylvain Boily <sboily@proformatique.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from amazon import EC2Conn
import time
from app.extensions import celery, db
from celery.signals import task_postrun, task_sent, task_success, task_prerun, task_failure
from deploy_amazon import deploy_xivo_on_amazon
from models import Servers_EC2


@task_sent.connect(sender='tasks.deploy_on_cloud')
def task_sent_handler(sender=None, task_id=None, task=None, args=None,
                      kwargs=None, **kwds):
    _update_status_in_db(args[0], 'failure')
    print('Got signal task_sent for task id %s' % (task_id, ))

@task_failure.connect(sender='tasks.deploy_on_cloud')
def task_sent_error(sender=None, task_id=None, task=None, args=None,
                      kwargs=None, **kwds):
    print('Got signal task_error for task id %s' % (task_id, ))


@task_postrun.connect
def close_session(*args, **kwargs):
    db.session.remove()

@task_prerun.connect
def t_prerun(sender=None, task_id=None, task=None, args=None, kwargs=None, **kwds):
    print('Got signal task_prerun with value : %s' % (task_id))

@task_success.connect
def t_success(sender, result, **kwargs):
    print('Got signal task_success for server : %s' % (result[0]))



@celery.task(name='tasks.deploy_on_cloud', ignore_result=False)
def deploy_on_cloud(id, config, ssh_key):
    _update_status_in_db(id, 'initializing')
    instance = create_new_instance_on_amazon(config)
    print 'Waiting for the amazon checking ...'
    _save_instance_in_db(id, instance)
    _update_status_in_db(id, 'checking')
    time.sleep(65)
    _update_status_in_db(id, 'installing')
    print 'Deploy !'
    deploy_xivo_on_amazon(instance.ip_address,ssh_key)
    print 'Finish !'

    _update_status_in_db(id, 'running')
    return (id, instance)

def _save_instance_in_db(id, instance):
    server_ec2 = Servers_EC2.query.get(id)
    server_ec2.address = instance.ip_address
    server_ec2.instance_ec2 = instance.id
    db.session.add(server_ec2)
    db.session.commit()

def _update_status_in_db(id, state):
    server_ec2 = Servers_EC2.query.get(id)
    server_ec2.status = state
    db.session.add(server_ec2)
    db.session.commit()

def undeploy_on_cloud(instance, config):
    instance = delete_instance_on_amazon(instance, config)

    return instance    

def create_new_instance_on_amazon(config):
    ec2 = EC2Conn(config)
    ec2.connect()
    return ec2.create_instance()

def delete_instance_on_amazon(instance_id, config):
    ec2 = EC2Conn(config)
    ec2.connect()
    return ec2.delete_instance(instance_id)
