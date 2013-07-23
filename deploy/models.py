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

from datetime import datetime
from app import db

class RegisterProviders(db.Model):
    __bind_key__ = 'deploy_base'
    __tablename__ = 'register_providers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    base_url = db.Column(db.String(200))
    classname = db.Column(db.String(200))
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    associate = db.relationship('AssociateProviders', backref='associate',
                                 lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<%d : %s>" % (self.id, self.name)

class AssociateProviders(db.Model):
    __bind_key__ = 'deploy_base'
    __tablename__ = 'associate_providers'

    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('register_providers.id'))
    organisation_id = db.Column(db.Integer)
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
