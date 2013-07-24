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

class ServersAmazon(Deploy_Servers, db.Model):
    __bind_key__ = 'deploy_amazon'
    __tablename__ = 'servers_amazon'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200))
    elastics_ip = db.Column(db.String(200))
    instance_params = db.Column(db.String(200), default='xivo')
    image_id = db.Column(db.String(200), default='ami-2c28ba45')
    instance_type = db.Column(db.String(200), default='t1.micro')
    status = db.Column(db.String(200))
    task_id = db.Column(db.String(200))
    configuration_id = db.Column(db.Integer, db.ForeignKey('provider_amazon.id'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<%d : %s (%s) - %s>" % (self.id, self.name, self.address, self.instance)

class ProviderAmazon(Providers, db.Model):
    __bind_key__ = 'deploy_amazon'
    __tablename__ = 'provider_amazon'
    id = db.Column(db.Integer, primary_key=True)
    access_key = db.Column(db.String(200))
    secret_key = db.Column(db.String(200))
    security_groups = db.Column(db.String(200), default='default')
    key_name = db.Column(db.String(200))
    ssh_key = db.Column(db.Text())
    servers = db.relationship('ServersAmazon', backref='servers',lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<%d : %s>" % (self.id, self.name)
