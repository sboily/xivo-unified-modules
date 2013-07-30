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
from datetime import datetime
from app.plugins.deploy.models_base import Providers, Deploy_Servers

class ServersOpenStack(Deploy_Servers, db.Model):
    __bind_key__ = 'deploy_openstack'
    __tablename__ = 'servers_openstack'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200))
    elastics_ip = db.Column(db.String(200))
    status = db.Column(db.String(200))
    task_id = db.Column(db.String(200))
    configuration_id = db.Column(db.Integer, db.ForeignKey('provider_openstack.id'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<%d : %s (%s) - %s>" % (self.id, self.name, self.address, self.instance)

class ProviderOpenStack(Providers, db.Model):
    __bind_key__ = 'deploy_openstack'
    __tablename__ = 'provider_openstack'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(200))
    password = db.Column(db.String(200))
    tenant = db.Column(db.String(200))
    api_url = db.Column(db.String(200))
    image_name = db.Column(db.String(200))
    flavor = db.Column(db.String(200))
    keypair_name = db.Column(db.String(200))
    keypair_private = db.Column(db.Text())
    subnet_name = db.Column(db.String(200))
    servers = db.relationship('ServersOpenStack', backref='servers',lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<%d : %s>" % (self.id, self.name)
