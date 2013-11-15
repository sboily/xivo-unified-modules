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

from app.helpers.restclient import client
from flask import g

class Voicemails(object):

    def connect(self):
        return client.RestClient(g.server.login, g.server.password)

    def list(self, url):
        conn = self.connect()
        return conn.get(url)

    def add(self, url, form):
        conn = self.connect()
        voicemail = { 'name' : form.name.data,
                      'context' : form.context.data,
                      'number' : form.number.data,
                      'email' : form.email.data,
                      'password' : form.password.data
                    }
        return conn.post(url, voicemail)

    def show(self, url):
        conn = self.connect()
        return conn.get(url)

    def edit(self, url, form):
        conn = self.connect()
        voicemail = { 'name' : form.name.data,
                      'context' : form.context.data,
                      'number' : form.number.data,
                      'email' : form.email.data,
                      'password' : form.password.data
                    }
        return conn.put(url, voicemail)

    def delete(self, url):
        conn = self.connect()
        return conn.delete(url)
