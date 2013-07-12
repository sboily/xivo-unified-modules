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

import time
from app.extensions import celery, db
from celery.signals import task_postrun, task_sent, task_failure
from app.models import Servers, Organisations, User
from register_class import registerclass
from models import RegisterProviders

#@task_sent.connect(sender='tasks.deploy_on_cloud')
#def task_sent_handler(sender=None, task_id=None, task=None, args=None,
#                      kwargs=None, **kwds):
#    _update_status_in_db(args[0], 'started')
#    print('Got signal task_sent for task id %s' % (task_id, ))
#
#@task_failure.connect(sender='tasks.deploy_on_cloud')
#def task_sent_error(sender=None, task_id=None, task=None, args=None,
#                      kwargs=None, **kwds):
#    _update_status_in_db(args[0], 'failed')
#    print('Got signal task_error for task id %s' % (task_id, ))
#
#@task_postrun.connect
#def close_session(*args, **kwargs):
#    db.session.remove()

@celery.task(name='tasks.deploy_on_cloud', ignore_result=False)
def deploy_on_cloud(provider, id):
    task_id = deploy_on_cloud.request.id
    provider = RegisterProviders.query.filter(RegisterProviders.name == provider.capitalize()) \
                                       .first()
    cls = registerclass(provider)
    cls.deploy_server(id, task_id)

def undeploy_on_cloud(provider, id):
    task_id = deploy_on_cloud.request.id
    provider = RegisterProviders.query.filter(RegisterProviders.name == provider.capitalize()) \
                                       .first()
    cls = registerclass(provider)
    cls.undeploy_server(id)
