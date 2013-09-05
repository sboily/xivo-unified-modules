#!/usr/bin/python
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

import httplib2
import urllib
from BeautifulSoup import BeautifulSoup
import getopt, sys

def get_ivr(host, username, password):
    url_ivr = "%s/ivr/shows" % host
    url_login = "%s/login" % host

    h = httplib2.Http(disable_ssl_certificate_validation=True)
    resp, content = h.request(url_login)
    soup = BeautifulSoup(content)

    csrf_token = soup.find('input', dict(name='csrf_token'))['value']

    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    headers.update({'Cookie': resp['set-cookie']})
    body = { 'username' : username, 'password' : password, 'submit' : 'Authentification', 'csrf_token' : csrf_token }
    resp, content = h.request(url_login, "POST", headers=headers, body=urllib.urlencode(body))

    headers = {'Cookie': resp['set-cookie']}
    resp, content = h.request(url_ivr, 'GET', headers=headers)

    soup = BeautifulSoup(content)

    csrf_token = None

    try:
        csrf_token = soup.find('input', dict(name='csrf_token'))['value']
    except:
        pass

    if csrf_token or content.find("myivr") == -1:
        print "; Sorry login or password is invalid or url doesn't exist !"
        print "; Please contact support !"
    else:
        content = content.replace('<br>', '\n')
        print content

def main():
    host = None
    username = None
    password = None

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:u:p:")
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)

    for o, a in opts:
        if o == "-h":
            host = a
        elif o == "-u":
            username = a
        elif o == "-p":
            password = a
        else:
            assert False, "unhandled option"

    if host and username and password:
        get_ivr( host, username, password)
    else:
        usage()

def usage():
    usage = """
    -h define the host (manage.xivo.fr)
    -u define the username
    -p define the password
    """

    print usage

if __name__ == "__main__":
    main()

