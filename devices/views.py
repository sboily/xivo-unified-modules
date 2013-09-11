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

from flask import render_template, session, flash, redirect, url_for, g, request
from flask.ext.login import login_required, current_user
from app import create_app as app, db
from app.models import Servers
from restclient import GET, POST, PUT, DELETE
from forms import DevicesForm
import json
import wtforms_json
from setup import bp_devices, devices

wtforms_json.init()

@bp_devices.before_request
def before_request():
    if current_user.is_authenticated():
        if hasattr(g, 'server'):
            g.url_rest = "https://%s:50051/%s/devices" %(g.server.address, g.server.protocol)
        else:
            flash('Sorry you need to choose a server !')
            return redirect(url_for('home.homepage'))
    else:
        print 'User need to be identified !'

@bp_devices.route('/devices')
@login_required
def list():
    my_devices = devices.api_actions(g.url_rest, "GET", g.server.login, g.server.password)
    print my_devices
    if not my_devices:
        flash('Sorry the server have not any correct json data !')
        return redirect(url_for('home.homepage'))
    return render_template('list.html', devices=my_devices['items'])

@bp_devices.route('/devices/add', methods=['GET', 'POST'])
@login_required
def add():
    userform = UserForm()
    if request.method == 'POST' and userform.validate_on_submit():
        _add_user(userform)
        flash('Device added')
        return redirect(url_for('devices.list'))
    return render_template('add.html', userform=userform)

@bp_devices.route('/devices/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    user = _get_user(id)
    userform = UserForm.from_json(user)
    form = UserForm(obj=user)
    if userform.is_submitted():
        _edit_user(form, id)
        return redirect(url_for("devices.list"))
    return render_template('edit.html', user=user, userform=userform)

@bp_devices.route('/devices/delete/<id>')
@login_required
def delete(id):
    _del_user(id)
    flash('Device delete !')
    return redirect(url_for("devices.list"))

def _check_json(json_value):
    try:
        check_json = json.loads(json_value)
    except ValueError, e:
        print 'Sorry there is no JSON response'
        return False
    return check_json

def _get_devices():
    try:
        devices_response = GET(g.url_rest_devices, credentials=(g.server.login, g.server.password), 
                                          headers={'Content-Type': 'application/json'}, 
                                          httplib_params={'timeout': 10, 'disable_ssl_certificate_validation' : True})
        return _check_json(devices_response)
    except:
        return False

def _get_user(id):
    try:
        user_response = GET(g.url_rest_user + id, credentials=(g.server.login, g.server.password),
                                                    headers={'Content-Type': 'application/json'}, 
                                                    httplib_params={'timeout': 10, 'disable_ssl_certificate_validation' : True})
        return _check_json(user_response)
    except:
        return False

def _del_user(id):
    try:
        del_response = DELETE(g.url_rest_user + id, credentials=(g.server.login, g.server.password),
                                                      headers={'Content-Type': 'application/json'}, 
                                                      httplib_params={'timeout': 10, 'disable_ssl_certificate_validation' : True})
        return del_response
    except:
        return False

def _add_user(userform):
    user = { 'firstname' : userform.firstname.data,
             'lastname' : userform.lastname.data,
             'username' : userform.username.data,
             'password' : userform.password.data
           }

    try:
        user_add = POST(g.url_rest_user,
                        params=user,
                        credentials=(g.server.login, g.server.password),
                        headers={'Content-Type': 'application/json'},
                        httplib_params={'timeout': 10, 'disable_ssl_certificate_validation' : True})
        return True
    except:
        return False

def _edit_user(userform, id):
    user = { 'firstname' : userform.firstname.data,
             'lastname' : userform.lastname.data,
             'username' : userform.username.data,
             'password' : userform.password.data
           }
    try:
        user_edit = PUT(g.url_rest_user + id,
                        params=user,
                        credentials=(g.server.login, g.server.password),
                        headers={'Content-Type': 'application/json'},
                        httplib_params={'timeout': 10, 'disable_ssl_certificate_validation' : True})
        return True
    except:
        return False
