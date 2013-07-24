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
from models import ProviderSsh, ServersSsh
from forms import SshForm
from celery.task.control import revoke

from fabric_ssh import deploy_xivo_on_ssh

class DeployOnSsh(Deploy):

    def __init__(self):
        Deploy.__init__(self)

    def setup(self, app):
        self.db_bind = 'deploy_ssh'
        mydbplugindir = os.path.join(app.config['BASEDIR'],'app/plugins/ssh/db/servers_ssh.db')
        app.config['SQLALCHEMY_BINDS'].update({self.db_bind : 'sqlite:///%s' % mydbplugindir})

        with app.app_context():
            db.create_all(bind=self.db_bind)

        self.register(app, {'name' : 'Ssh',
                            'db_bind' : self.db_bind,
                            'base_url' : '/ssh',
                            'classname' : 'DeployOnSsh',
                            'organisation_id' : 0
                            })

    def get_configurations(self):
        configuration =  ProviderSsh.query.filter(ProviderSsh.organisation_id == g.user_organisation.id) \
                                             .order_by(ProviderSsh.name)
        return configuration

    def add_provider(self, form):
        provider = ProviderSsh(form.name.data)
        provider.access_key = form.access_key.data
        provider.secret_key = form.secret_key.data
        provider.key_name = form.key_name.data
        provider.ssh_key = form.ssh_key.data
        provider.organisation_id = g.user_organisation.id

        db.session.add(provider)
        db.session.commit()

    def delete_provider(self, id):
        provider = ProviderSsh.query.filter(ProviderSsh.id == id).first()

        if provider:
            db.session.delete(provider)
            db.session.commit()

    def get_provider(self, id):
        return ProviderSsh.query.filter(ProviderSsh.id == id).first()

    def edit_provider(self, form, provider):
        form.populate_obj(provider)
        db.session.add(provider)
        db.session.commit()
        
    def get_servers(self):
        servers =  ServersSsh.query.filter(ServersSsh.organisation_id == g.user_organisation.id) \
                                      .order_by(ServersSsh.name)
        return servers

    def add_server(self, form):
        provider = ServersSsh(form.name.data)
        provider.organisation_id = g.user_organisation.id
        provider.servers = form.configuration.data

        db.session.add(provider)
        db.session.commit()

    def delete_server(self, id):
        server = ServersSsh.query.get_or_404(id)
        db.session.delete(server)
        db.session.commit()

    def deploy_server(self, id, task_id, user_info):
        print 'deploy ...'
        self._update_status_in_db(id, 'initializing')
        server = ServersSsh.query.get(id)
        self._init_deploy(server, id, task_id)
        config = self._create_config(server)
        self._update_status_in_db(id, 'installing')
        print 'Deploy !'
        deploy_xivo_on_ssh(server.servers.login, server.servers.password, server.ip)
        print 'Finish !'

        self._update_status_in_db(id, 'running')
        user_info.update({'name' : server.name})
        self._add_server_in_servers(server.ip, user_info)
        return (id, server.ip)

    def undeploy_server(self, id):
        server = ServersSsh.query.filter(ServersSsh.id == id).first()

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
        server = ServersSsh.query.get(id)
        server.status = state
        db.session.add(server_ec2)
        db.session.commit()

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

    def _save_instance_in_db(self, id, ip):
        server = ServersSsh.query.get(id)
        server.address = ip
        server.instance = '-'
        db.session.add(server)
        db.session.commit()

    def stop_task(self, id):
        server = ServersSsh.query.filter(ServersSsh.id == id).first()
        revoke(server.task_id, terminate=True)
        server.status = None
        server.address = None
        server.instance = None
        server.installed_time = None
        db.session.add(server)
        db.session.commit()
