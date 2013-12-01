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
from setup import bp_call_logs, call_logs

import csv

@bp_call_logs.before_request
def before_request():
    if current_user.is_authenticated():
        if hasattr(g, 'server'):
            g.url_rest = "https://%s:50051/%s/call_logs" %(g.server.address, g.server.protocol)
        else:
            flash('Sorry you need to choose a server !')
            return redirect(url_for('home.homepage'))
    else:
        print 'User need to be identified !'

@bp_call_logs.route('/call_logs')
@login_required
def list():
    my_call_logs = call_logs.list(g.url_rest)
    print my_call_logs
    if not my_call_logs:
        flash('Sorry the server have not any correct json data !')
        return redirect(url_for('home.homepage'))
    pouet = csv.DictReader(my_call_logs, quoting=csv.QUOTE_NONE)
    for row in pouet:
        print row
    return render_template('call_logs_list.html', call_logs=csv.DictReader(my_call_logs))
