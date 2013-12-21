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

class ServerLdap(db.Model):
    __bind_key__ = 'addressbook'
    __tablename__ = 'server_ldap'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    host = db.Column(db.Text())
    basedn = db.Column(db.Text())
    login = db.Column(db.Text())
    secret = db.Column(db.Text())
    organisation_id = db.Column(db.Integer)
    created_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<%d : %s>" % (self.id, self.name)
