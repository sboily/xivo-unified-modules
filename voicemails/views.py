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
from forms import VoicemailForm
import wtforms_json
from setup import bp_voicemails, voicemails

wtforms_json.init()

@bp_voicemails.before_request
def before_request():
    if current_user.is_authenticated():
        if hasattr(g, 'server'):
            g.url_rest = "https://%s:50051/1.0/voicemails" %(g.server.address)
        else:
            flash('Sorry you need to choose a server !')
            return redirect(url_for('home.homepage'))
    else:
        print 'User need to be identified !'

@bp_voicemails.route('/voicemails')
@login_required
def list():
    my_voicemails = voicemails.list(g.url_rest)
    if not my_voicemails:
        flash('Sorry the server have not any correct json data !')
        return redirect(url_for('home.homepage'))
    return render_template('voicemails_list.html', voicemails=my_voicemails['items'])

@bp_voicemails.route('/voicemails/add', methods=['GET', 'POST'])
@login_required
def add():
    form = VoicemailForm()
    if request.method == 'POST' and form.validate_on_submit():
        voicemails.add(g.url_rest, form)
        flash('Voicemail added')
        return redirect(url_for('voicemails.list'))
    return render_template('voicemail_add.html', form=form)

@bp_voicemails.route('/voicemails/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    my_voicemails = voicemails.show(g.url_rest + "/" + id)
    form = VoicemailForm.from_json(my_voicemails)
    if form.is_submitted():
        voicemails.edit(g.url_rest + "/" + id, VoicemailForm(obj=voicemails))
        return redirect(url_for("voicemails.list"))
    return render_template('voicemail_edit.html', voicemails=my_voicemails, form=form)

@bp_voicemails.route('/voicemails/delete/<id>')
@login_required
def delete(id):
    voicemails.delete(g.url_rest + "/" + id)
    flash('Voicemail delete !')
    return redirect(url_for("voicemails.list"))
