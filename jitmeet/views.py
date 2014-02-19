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

from flask import render_template, url_for, redirect
from flask.ext.login import login_required, current_user
from setup import bp_jitmeet, jitmeet
from forms import RoomForm

@bp_jitmeet.route('/jitmeet')
@login_required
def list():
    room = jitmeet.list()
    return render_template('list.html', room=room)

@bp_jitmeet.route('/jitmeet/add', methods=['GET', 'POST'])
@login_required
def add():
    form = RoomForm()
    if form.validate_on_submit():
        jitmeet.add(form.name.data)
        return redirect(url_for('jitmeet.list'))
    return render_template('add.html', form=form)

@bp_jitmeet.route('/jitmeet/delete/<id>')
@login_required
def delete(id):
    jitmeet.delete(id)
    return redirect(url_for('jitmeet.list'))

@bp_jitmeet.route('/jitmeet_<id>')
def open(id):
    is_anonymous_content=0
    if current_user.is_anonymous:
        is_anonymous_content=1
    return render_template('jitmeet.html', is_anonymous_content=is_anonymous_content)

@bp_jitmeet.route('/jitmeet/invite/<id>')
@login_required
def invite(id):
    return render_template('invite.html', id=id)

@bp_jitmeet.route('/jitmeet/chromeonly')
@login_required
def chromeonly():
    return render_template('chromeonly.html')

@bp_jitmeet.route('/jitmeet/webrtcrequired')
@login_required
def webrtcrequired():
    return render_template('webrtcrequired.html')
