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
from forms import CTI_ProfilesForm
from setup import bp_cti_profiles, cti_profiles

@bp_cti_profiles.before_request
def before_request():
    if current_user.is_authenticated():
        if hasattr(g, 'server'):
            g.url_rest = "https://%s:50051/%s/cti_profiles" %(g.server.address, g.server.protocol)
        else:
            flash('Sorry you need to choose a server !')
            return redirect(url_for('home.homepage'))
    else:
        print 'User need to be identified !'

@bp_cti_profiles.route('/cti_profiles')
@login_required
def list():
    my_cti_profiles = cti_profiles.list(g.url_rest)
    if not my_cti_profiles:
        flash('Sorry the server have not any correct json data !')
        return redirect(url_for('home.homepage'))
    return render_template('cti_profiles_list.html', cti_profiles=my_cti_profiles['items'])

@bp_cti_profiles.route('/cti_profiles/<id>')
@login_required
def show(id):
    my_cti_profiles = cti_profiles.show(g.url_rest + "/" + id)
    form = CTI_ProfilesForm.from_json(my_cti_profiles)
    return render_template('cti_profiles_show.html', cti_profiles=my_cti_profiles, form=form)
