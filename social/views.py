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

from flask import render_template, redirect, url_for
from flask.ext.login import login_required
from forms import SocialForm
from setup import bp_social, social

@bp_social.route('/social', methods=['GET', 'POST'])
@login_required
def be():
    form = SocialForm()
    msg = social.list()
    if form.validate_on_submit():
        social.add(form.status.data)
        return redirect(url_for('social.be'))
    return render_template('social.html', form=form, msg=msg)
