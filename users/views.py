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

from flask import render_template, flash, redirect, url_for, g, request
from flask.ext.login import login_required, current_user
from forms import UserForm
from setup import bp_users, users

@bp_users.before_request
def before_request():
    if current_user.is_authenticated():
        if hasattr(g, 'server'):
            g.url_rest = "https://%s:50051/%s/users" %(g.server.address, g.server.protocol)
        else:
            flash('Sorry you need to choose a server !')
            return redirect(url_for('home.homepage'))
    else:
        print 'User need to be identified !'

@bp_users.route('/users')
@login_required
def list():
    my_users = users.list(g.url_rest)
    if not my_users:
        flash('Sorry the server have not any correct json data !')
        return redirect(url_for('home.homepage'))
    return render_template('users_list.html', users=my_users['items'])

@bp_users.route('/users/add', methods=['GET', 'POST'])
@login_required
def add():
    form = UserForm()
    if request.method == 'POST' and form.validate_on_submit():
        users.add(g.url_rest, form)
        flash('User added')
        return redirect(url_for('users.list'))
    return render_template('user_add.html', form=form)

@bp_users.route('/users/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    my_users = users.show(g.url_rest + "/" + id)
    form = UserForm.from_json(my_users)
    if form.is_submitted():
        users.edit(g.url_rest + "/" + id, UserForm(obj=users))
        return redirect(url_for("users.list"))
    return render_template('user_edit.html', users=my_users, form=form)

@bp_users.route('/users/delete/<id>')
@login_required
def delete(id):
    users.delete(g.url_rest + "/" + id)
    flash('User delete !')
    return redirect(url_for("users.list"))
