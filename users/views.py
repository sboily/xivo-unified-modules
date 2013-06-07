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

from flask import render_template, Blueprint, session, flash, redirect, url_for, g, request
from flask.ext.login import login_required, current_user
from app import app, db
from app.core.server.models import Servers
from restclient import GET, POST, PUT, DELETE
from forms import UserForm
import json
import wtforms_json

users = Blueprint('users', __name__, template_folder='templates/users')
wtforms_json.init()

@users.before_request
def before_request():
    if current_user.is_authenticated():
        if hasattr(g, 'server'):
            g.url_rest_user = "https://%s:50051/1.0/users/" % g.server.address
        else:
            flash('Sorry you need to choose a server !')
            return redirect(url_for("home"))
    else:
        print 'User need to be identified !'

@users.route('/users')
@login_required
def user():
    users = _get_users()
    if not users:
        flash('Sorry the server have not any correct json data !')
        return redirect(url_for("home"))
    return render_template('users.html', users=users['items'])

@users.route('/users/add', methods=['GET', 'POST'])
@login_required
def user_add():
    userform = UserForm()
    if request.method == 'POST' and userform.validate_on_submit():
        _add_user(userform)
        flash('User added')
        return redirect(url_for("users.user"))
    return render_template('users_add.html', userform=userform)

@users.route('/users/<id>', methods=['GET', 'POST'])
@login_required
def user_edit(id):
    user = _get_user(id)
    userform = UserForm.from_json(user)
    form = UserForm(obj=user)
    if userform.is_submitted():
        _edit_user(form, id)
        return redirect(url_for("users.user"))
    return render_template('users_edit.html', user=user, userform=userform)

@users.route('/users/del/<id>')
@login_required
def user_del(id):
    _del_user(id)
    flash('User delete !')
    return redirect(url_for("users.user"))

def _check_json(json_value):
    try:
        check_json = json.loads(json_value)
    except ValueError, e:
        print 'Sorry there is no JSON response'
        return False
    return check_json

def _get_users():
    users_response = GET(g.url_rest_user, credentials=(g.server.login, g.server.password), 
                                          headers={'Content-Type': 'application/json'}, 
                                          httplib_params={'disable_ssl_certificate_validation' : True})
    return _check_json(users_response)

def _get_user(id):
    user_response = GET(g.url_rest_user + id, credentials=(g.server.login, g.server.password),
                                                    headers={'Content-Type': 'application/json'}, 
                                                    httplib_params={'disable_ssl_certificate_validation' : True})
    return _check_json(user_response)

def _del_user(id):
    del_response = DELETE(g.url_rest_user + id, credentials=(g.server.login, g.server.password),
                                                      headers={'Content-Type': 'application/json'}, 
                                                      httplib_params={'disable_ssl_certificate_validation' : True})
    return del_response

def _add_user(userform):
    user = { 'firstname' : userform.firstname.data,
             'lastname' : userform.lastname.data,
             'username' : userform.username.data,
             'password' : userform.password.data
           }
    user_add = POST(g.url_rest_user,
                    params=user,
                    credentials=(g.server.login, g.server.password),
                    headers={'Content-Type': 'application/json'},
                    httplib_params={'disable_ssl_certificate_validation' : True})
    return True

def _edit_user(userform, id):
    user = { 'firstname' : userform.firstname.data,
             'lastname' : userform.lastname.data,
             'username' : userform.username.data,
             'password' : userform.password.data
           }
    user_edit = PUT(g.url_rest_user + id,
                    params=user,
                    credentials=(g.server.login, g.server.password),
                    headers={'Content-Type': 'application/json'},
                    httplib_params={'disable_ssl_certificate_validation' : True})
    return True
