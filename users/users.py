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

from restclient import GET, POST, PUT, DELETE
import json

class Users(object):

    def __init__(self):
        self.httplib_params = {'timeout': 10, 'disable_ssl_certificate_validation' : True}
        self.headers = {'Content-Type': 'application/json'}

    def check_json(self, value):
        try:
            check_json = json.loads(value)
        except ValueError, e:
            print 'Sorry there is no JSON response'
            return False

        return check_json

    def api_actions(self, url, method, login, password, data=None):
        if (method == 'GET'):
            response = GET(url, credentials=(login, password),
                                headers=self.headers,
                                httplib_params=self.httplib_params)
        elif (method == 'DELETE'):
            response = DELETE(url, credentials=(login, password),
                                   headers=self.headers,
                                   httplib_params=self.httplib_params)
        elif (method == 'POST'):
            response = POST(url, credentials=(login, password),
                                 headers=self.headers,
                                 httplib_params=self.httplib_params,
                                 params=data)
        elif (method == 'PUT'):
            response = PUT(url, credentials=(login, password),
                                 headers=self.headers,
                                 httplib_params=self.httplib_params,
                                 params=data)
        else:
            print "Error this method is not supported"
            return False

        return self.check_json(response)

    def add(self, form):
        user = { 'firstname' : form.firstname.data,
                 'lastname' : form.lastname.data,
                 'username' : form.username.data,
                 'password' : form.password.data
               }

    def edit(self, form, id):
        user = { 'firstname' : form.firstname.data,
                 'lastname' : form.lastname.data,
                 'username' : form.username.data,
                 'password' : form.password.data
               }
