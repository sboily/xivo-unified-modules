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

from flask import render_template, flash, redirect, url_for
from flask.ext.login import login_required
from flask.ext.babel import gettext as _
from setup import bp_openstack, openstack
from forms import OpenStackForm, OpenStackServerForm

@bp_openstack.route('/openstack')
@login_required
def provider_list():
    list = openstack.get_configurations()
    return render_template('openstack_provider_list.html', list=list)

@bp_openstack.route('/openstack/add', methods=['GET', 'POST'])
@login_required
def provider_add():
    form = OpenStackForm()
    if form.validate_on_submit():
        openstack.add_provider(form)
        flash(_('OpenStack informations added'))
        return redirect(url_for("openstack.provider_list"))
    return render_template('openstack_provider_add.html', form=form)

@bp_openstack.route('/openstack/edit/<id>', methods=['GET', 'POST'])
@login_required
def provider_edit(id):
    provider = openstack.get_provider(id)
    form = OpenStackForm(obj=provider)
    if form.validate_on_submit():
        openstack.edit_provider(form, provider)
        flash(_('OpenStack provider edit'))
        return redirect(url_for("openstack.provider_list"))
    return render_template('openstack_provider_edit.html', form=form)

@bp_openstack.route('/openstack/del/<id>')
@login_required
def provider_delete(id):
    openstack.delete_provider(id)
    flash(_('OpenStack information deleted'))
    return redirect(url_for("openstack.provider_list"))

@bp_openstack.route('/openstack/server/add', methods=['GET', 'POST'])
@login_required
def server_add():
    form = OpenStackServerForm()
    if form.validate_on_submit():
        openstack.add_server(form)
        flash(_('OpenStack server added'))
        return redirect(url_for('deploy.deploy_list'))
    return render_template('openstack_server_add.html', form=form)

@bp_openstack.route('/openstack/server/delete/<id>')
@login_required
def server_delete(id):
    openstack.delete_server(id)
    flash(_('OpenStack server deleted'))
    return redirect(url_for('deploy.deploy_list'))

@bp_openstack.route('/openstack/server/deploy/<id>')
@login_required
def server_deploy(id):
    openstack.deploy_server(id)
    flash(_('OpenStack server deploy launched'))
    return redirect(url_for('deploy.deploy_list'))
