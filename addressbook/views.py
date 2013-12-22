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
from setup import bp_addressbook, addressbook
from forms import AddressBookForm, AddressBookServerLdapForm
from flask.ext.babel import gettext as _

@bp_addressbook.route('/addressbook')
@login_required
def list():
    addrbook = addressbook.list()
    return render_template('addressbook_list.html', addressbook=addrbook)

@bp_addressbook.route('/addressbook/show/<uid>')
@login_required
def show(uid):
    contact = addressbook.show(uid)
    form = AddressBookForm(**contact)
    return render_template('addressbook_show.html', contact=contact, form=form)

@bp_addressbook.route('/addressbook/get/image/<uid>')
@login_required
def get_image(uid):
    return addressbook.get_image(uid)

@bp_addressbook.route('/addressbook/server/configure', methods=['GET', 'POST'])
@login_required
def configure_ldap_server():
    server = addressbook.get_server()
    form = AddressBookServerLdapForm(obj=server)
    if form.validate_on_submit():
        if server:
            addressbook.edit_server(form, server)
            flash(_('Server LDAP edited'))
        else:
            addressbook.add_server(form)
            flash(_('Server LDAP added'))
        return redirect(url_for('addressbook.list'))
    return render_template('addressbook_server_configure.html', form=form)
