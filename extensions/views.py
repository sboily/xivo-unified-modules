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
from forms import ExtensionForm
from setup import bp_extensions, extensions

@bp_extensions.before_request
def before_request():
    if current_user.is_authenticated():
        if hasattr(g, 'server'):
            g.url_rest = "https://%s:50051/%s/extensions" %(g.server.address, g.server.protocol)
        else:
            flash('Sorry you need to choose a server !')
            return redirect(url_for('home.homepage'))
    else:
        print 'User need to be identified !'

@bp_extensions.route('/extensions')
@login_required
def list():
    my_extensions = extensions.list(g.url_rest)
    if not my_extensions:
        flash('Sorry the server have not any correct json data !')
        return redirect(url_for('home.homepage'))
    return render_template('extensions_list.html', extensions=my_extensions['items'])

@bp_extensions.route('/extensions/add', methods=['GET', 'POST'])
@login_required
def add():
    form = ExtensionForm()
    if request.method == 'POST' and form.validate_on_submit():
        extensions.add(g.url_rest, form)
        flash('Extension added')
        return redirect(url_for('extensions.list'))
    return render_template('extension_add.html', form=form)

@bp_extensions.route('/extensions/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    my_extensions = extensions.show(g.url_rest + "/" + id)
    form = ExtensionForm.from_json(my_extensions)
    if form.is_submitted():
        extensions.edit(g.url_rest + "/" + id, ExtensionForm(obj=extensions))
        return redirect(url_for("extensions.list"))
    return render_template('extension_edit.html', extensions=my_extensions, form=form)

@bp_extensions.route('/extensions/delete/<id>')
@login_required
def delete(id):
    extensions.delete(g.url_rest + "/" + id)
    flash('Extension delete !')
    return redirect(url_for("extensions.list"))
