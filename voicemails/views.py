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
from app import create_app as app, db
from app.models import Servers
from restclient import GET, POST, PUT, DELETE
import json
from forms import VoicemailForm
from setup import voicemails
import wtforms_json

wtforms_json.init()

@voicemails.before_request
def before_request():
    if current_user.is_authenticated():
        if hasattr(g, 'server'):
            g.url_rest_user = "https://%s:50051/1.0/voicemails/" % g.server.address
        else:
            flash('Sorry you need to choose a server !')
            return redirect(url_for('home.homepage'))
    else:
        print 'User need to be identified !'

@voicemails.route('/voicemails')
@login_required
def voicemail():
    voicemails = _get_voicemails()
    if not voicemails:
        flash('Sorry the server have not any correct json data !')
        return redirect(url_for('home.homepage'))
    return render_template('voicemails.html', voicemails=voicemails['items'])

@voicemails.route('/voicemails/add', methods=['GET', 'POST'])
@login_required
def voicemail_add():
    voicemailform = VoicemailForm()
    if request.method == 'POST' and voicemailform.validate_on_submit():
        _add_voicemail(voicemailform)
        flash('Voicemail added')
        return redirect(url_for("voicemails.voicemail"))
    return render_template('voicemails_add.html', voicemailform=voicemailform)

@voicemails.route('/voicemails/<id>', methods=['GET', 'POST'])
@login_required
def voicemail_edit(id):
    voicemail = _get_voicemail(id)
    if voicemail:
        voicemailform = VoicemailForm.from_json(voicemail)
        form = VoicemailForm(obj=voicemail)
        if voicemailform.is_submitted():
            _edit_voicemail(form, id)
            return redirect(url_for("voicemails.voicemail"))
        return render_template('voicemail_edit.html', voicemail=voicemail, voicemailform=voicemailform)
    else:
        flash('Sorry edit voicemail is not implemented !')
        return redirect(url_for("voicemails.voicemail"))

@voicemails.route('/voicemails/del/<id>')
@login_required
def voicemail_del(id):
    _del_voicemail(id)
    flash('Voicemail delete !')
    return redirect(url_for("voicemails.voicemail"))

def _check_json(json_value):
    try:
        check_json = json.loads(json_value)
    except ValueError, e:
        print 'Sorry there is no JSON response'
        return False
    return check_json

def _get_voicemails():
    voicemails_response = GET(g.url_rest_user, credentials=(g.server.login, g.server.password), 
                                          headers={'Content-Type': 'application/json'}, 
                                          httplib_params={'disable_ssl_certificate_validation' : True})
    return _check_json(voicemails_response)

def _get_voicemail(id):
    voicemail_response = GET(g.url_rest_user + id, credentials=(g.server.login, g.server.password),
                                                    headers={'Content-Type': 'application/json'}, 
                                                    httplib_params={'disable_ssl_certificate_validation' : True})
    return _check_json(voicemail_response)

def _del_voicemail(id):
    del_response = DELETE(g.url_rest_user + id, credentials=(g.server.login, g.server.password),
                                                      headers={'Content-Type': 'application/json'}, 
                                                      httplib_params={'disable_ssl_certificate_validation' : True})
    return del_response

def _add_voicemail(voicemailform):
    voicemail = { 'mailbox' : voicemailform.mailbox.data,
                  'email' : voicemailform.email.data,
                  'password' : voicemailform.password.data
           }
    voicemail_add = POST(g.url_rest_user,
                    params=voicemail,
                    credentials=(g.server.login, g.server.password),
                    headers={'Content-Type': 'application/json'},
                    httplib_params={'disable_ssl_certificate_validation' : True})
    return True

def _edit_voicemail(voicemailform, id):
    voicemail = { 'mailbox' : voicemailform.mailbox.data,
                  'email' : voicemailform.email.data,
                  'password' : voicemailform.password.data
           }
    voicemail_edit = PUT(g.url_rest_user + id,
                    params=voicemail,
                    credentials=(g.server.login, g.server.password),
                    headers={'Content-Type': 'application/json'},
                    httplib_params={'disable_ssl_certificate_validation' : True})
    return True
