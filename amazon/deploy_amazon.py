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
from celery.task.control import revoke
import os

from app.plugins.deploy.deploy_base import Deploy
from models import ProviderAmazon, ServersAmazon

class DeployOnAmazon(Deploy):

    def __init__(self):
        Deploy.__init__(self)
        self.db_bind = 'deploy_amazon'

    def setup(self, app):

        mydbplugindir = os.path.join(app.config['BASEDIR'],'app/plugins/amazon/db/servers_amazon.db')
        app.config['SQLALCHEMY_BINDS'].update({'deploy_amazon': 'sqlite:///%s' % mydbplugindir})

        self.register({'name' : 'Amazon', 'cls' : self, 'db_bind' : 'deploy_amazon'})

    def init_db(self):
        print 'CREATE DB'
        db.create_all(bind=self.db_bind)

    def get_servers(self):
        self.init_db()
        servers =  ProviderAmazon.query.filter(ProviderAmazon.organisation_id == g.user_organisation.id) \
                                       .order_by(ProviderAmazon.name)
        return servers

    def add_provider(self, form):
        provider = ProviderAmazon(form.name.data)
        provider.access_key = form.access_key.data
        provider.secret_key = form.secret_key.data
        provider.key_name = form.key_name.data
        provider.ssh_key = form.ssh_key.data
        provider.organisation_id = g.user_organisation.id

        db.session.add(provider)
        db.session.commit()

    def delete_provider(self, id):
        provider = ProviderAmazon.query.filter(ProviderAmazon.id == id).first()

        if provider:
            db.session.delete(provider)
            db.session.commit()
        
    def create_config(self, sql_object):
        config = { 'access_key' : sql_object.servers.access_key,
                   'secret_key' : sql_object.servers.secret_key,
                   'elastics_ip' : sql_object.elastics_ip,
                   'instance_params' : sql_object.instance_params,
                   sql_object.instance_params : { 'image_id' : sql_object.image_id,
                                                  'instance_type' : sql_object.instance_type,
                                                  'security_groups' : [sql_object.servers.security_groups],
                                                  'key_name' : sql_object.servers.key_name,
                                                }
                 }

        return config

    def stop_task(self, id):
        server_ec2 = Servers_EC2.query.filter(Servers_EC2.id == id).first()
        revoke(server_ec2.task_id, terminate=True)
        server_ec2.status = None
        server_ec2.address = None
        server_ec2.instance_ec2 = None
        server_ec2.installed_time = None
        db.session.add(server_ec2)
        db.session.commit()
    

    def undeploy(self, id):
        server_ec2 = Servers_EC2.query.filter(Servers_EC2.id == id).first()

        if server_ec2.instance_ec2:
            config = self.create_config(server_ec2)
            inst = undeploy_on_cloud(server_ec2.instance_ec2, config)

        if server_ec2:
            db.session.delete(server_ec2)
            db.session.commit()

    def deploy(self, id):
        server_ec2 = Servers_EC2.query.filter(Servers_EC2.id == id).first()
        config = self.create_config(server_ec2)

        user_info = {'user_id' : g.user.id, 'organisation_id' : g.user_organisation.id, 'name' : server_ec2.name}

        task = deploy_on_cloud.apply_async((id, config, server_ec2.servers.ssh_key, user_info))
        server_ec2.task_id = task.task_id
        server_ec2.installed_time = datetime.datetime.utcnow()
        db.session.add(server_ec2)
        db.session.commit()
