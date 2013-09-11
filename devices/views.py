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
from forms import DeviceForm
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
    if not my_devices:
        flash('Sorry the server have not any correct json data !')
        return redirect(url_for('home.homepage'))
    return render_template('list.html', devices=my_devices['items'])

@bp_devices.route('/devices/add', methods=['GET', 'POST'])
@login_required
def add():
    form = DeviceForm()
    if request.method == 'POST' and form.validate_on_submit():
        devices.api_ations(g.url_rest, "POST", g.server.login, g.server.password, form)
        flash('Device added')
        return redirect(url_for('devices.list'))
    return render_template('add.html', form=form)

@bp_devices.route('/devices/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    my_devices = devices.api_actions(g.url_rest + "/" + id, "GET", g.server.login, g.server.password)
    form = DeviceForm.from_json(my_devices)
    if form.is_submitted():
        devices.edit(DeviceForm(obj=devices), id)
        return redirect(url_for("devices.list"))
    return render_template('edit.html', devices=my_devices, form=form)

@bp_devices.route('/devices/delete/<id>')
@login_required
def delete(id):
    devices.api_actions(g.url_rest + "/" + id, "DELETE", g.server.login, g.server.password)
    flash('Device delete !')
    return redirect(url_for("devices.list"))
