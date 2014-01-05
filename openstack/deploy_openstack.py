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

from app import db
from flask import g
import datetime
import os
import time

from app.plugins.deploy.deploy_base import Deploy
from app.models import User, Servers, Organisations
from models import ProviderOpenStack, ServersOpenStack
from forms import OpenStackForm
from celery.task.control import revoke
from flask.ext.login import current_user

from openstack import OpenStackConn
from fabric_openstack import deploy_xivo_on_openstack

class DeployOnOpenStack(Deploy):

    def __init__(self):
        Deploy.__init__(self)

    def setup(self, app):
        self.db_bind = 'deploy_openstack'
        mydbplugindir = os.path.join(app.config['BASEDIR'],'app/plugins/openstack/db/servers_openstack.db')
        app.config['SQLALCHEMY_BINDS'].update({self.db_bind : 'sqlite:///%s' % mydbplugindir})

        with app.app_context():
            db.create_all(bind=self.db_bind)

        self.register(app, {'name' : 'Openstack',
                            'db_bind' : self.db_bind,
                            'base_url' : '/openstack',
                            'classname' : 'DeployOnOpenStack',
                            })

    def get_configurations(self):
        configuration =  ProviderOpenStack.query.filter(ProviderOpenStack.organisation_id == current_user.organisation_id) \
                                             .order_by(ProviderOpenStack.name)
        return configuration

    def add_provider(self, form):
        provider = ProviderOpenStack(form.name.data)
        form.populate_obj(provider)
        provider.organisation_id = current_user.organisation_id
        db.session.add(provider)
        db.session.commit()

    def delete_provider(self, id):
        provider = ProviderOpenStack.query.filter(ProviderOpenStack.id == id).first()

        if provider:
            db.session.delete(provider)
            db.session.commit()

    def get_provider(self, id):
        return ProviderOpenStack.query.filter(ProviderOpenStack.id == id).first()

    def edit_provider(self, form, provider):
        form.populate_obj(provider)
        db.session.add(provider)
        db.session.commit()
        
    def get_servers(self):
        servers =  ServersOpenStack.query.filter(ServersOpenStack.organisation_id == current_user.organisation_id) \
                                      .order_by(ServersOpenStack.name)
        return servers

    def add_server(self, form):
        provider = ServersOpenStack(form.name.data)
        provider.organisation_id = current_user.organisation_id
        provider.servers = form.configuration.data

        db.session.add(provider)
        db.session.commit()

    def delete_server(self, id):
        server = ServersOpenStack.query.get_or_404(id)
        db.session.delete(server)
        db.session.commit()

    def deploy_server(self, id, task_id, user_info):
        print 'deploy ...'
        self._update_status_in_db(id, 'initializing')
        server = ServersOpenStack.query.get(id)
        self._init_deploy(server, id, task_id)
        config = self._create_config(server)
        (instance, ip) = self._create_new_instance_on_openstack(config)
        print 'Waiting for the openstack checking ...'
        self._save_instance_in_db(id, instance, ip)
        self._update_status_in_db(id, 'checking')
        time.sleep(15)
        self._update_status_in_db(id, 'installing')
        print 'Deploy !'
        deploy_xivo_on_openstack(ip, server.servers.keypair_private)
        print 'Finish !'

        self._update_status_in_db(id, 'running')
        user_info.update({'name' : server.name})
        self._add_server_in_servers(ip, user_info)
        return (id, instance)

    def undeploy_server(self, id):
        server = ServersOpenStack.query.filter(ServersOpenStack.id == id).first()

        if server.instance:
            config = self._create_config(server)
            inst = undeploy_on_cloud(server.instance, config)

        if server:
            db.session.delete(server)
            db.session.commit()


    def _init_deploy(self, server, id, task_id):
        server.installed_time = datetime.datetime.utcnow()
        server.task_id = task_id
        db.session.add(server)
        db.session.commit()

    def _update_status_in_db(self, id, state):
        server = ServersOpenStack.query.get(id)
        server.status = state
        db.session.add(server)
        db.session.commit()

    def _create_new_instance_on_openstack(self, config):
        ops = OpenStackConn(config)
        ops.connect()
        return ops.create_instance()


    def _add_server_in_servers(self, ip, user_info):
        server = Servers(name=user_info['name'], address=ip)
        org = Organisations.query.get(user_info['organisation_id'])
        user = User.query.get(user_info['user_id'])

        server.login = 'admin'
        server.password = 'proformatique'
        server.users = [user]
        server.organisation_id = org.id

        db.session.add(server)
        db.session.commit()

    def _save_instance_in_db(self, id, instance, ip):
        server = ServersOpenStack.query.get(id)
        server.address = ip
        server.instance = instance.id
        db.session.add(server)
        db.session.commit()

    def _create_config(self, server):
        config = {'login' : server.servers.login,
                  'password' : server.servers.password,
                  'tenant' : server.servers.tenant,
                  'api' : server.servers.api_url,
                  'image' : server.servers.image_name,
                  'flavor' : server.servers.flavor,
                  'keypair' : server.servers.keypair_name,
                  'name' : server.name,
                  'subnet' : server.servers.subnet_name
                 }

        return config

    def _delete_instance_on_openstack(self, instance_id, config):
        ops = OpenStackConn(config)
        ops.connect()
        return ops.delete_instance(instance_id)

    def stop_task(self, id):
        server = ServersOpenStack.query.filter(ServersOpenStack.id == id).first()
        revoke(server.task_id, terminate=True)
        server.status = None
        server.address = None
        server.instance = None
        server.installed_time = None
        db.session.add(server)
        db.session.commit()
