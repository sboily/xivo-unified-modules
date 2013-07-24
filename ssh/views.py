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
from setup import bp_ssh, ssh
from forms import SshForm, SshServerForm

@bp_amazon.route('/ssh')
@login_required
def provider_list():
    list = ssh.get_configurations()
    return render_template('ssh_provider_list.html', list=list)

@bp_amazon.route('/ssh/add', methods=['GET', 'POST'])
@login_required
def provider_add():
    form = AmazonForm()
    if form.validate_on_submit():
        ssh.add_provider(form)
        flash(_('Ssh informations added'))
        return redirect(url_for("ssh.provider_list"))
    return render_template('ssh_provider_add.html', form=form)

@bp_amazon.route('/ssh/edit/<id>', methods=['GET', 'POST'])
@login_required
def provider_edit(id):
    provider = ssh.get_provider(id)
    form = SshForm(obj=provider)
    if form.validate_on_submit():
        ssh.edit_provider(form, provider)
        flash(_('Ssh provider edit'))
        return redirect(url_for("ssh.provider_list"))
    return render_template('ssh_provider_edit.html', form=form)

@bp_amazon.route('/ssh/del/<id>')
@login_required
def provider_delete(id):
    ssh.delete_provider(id)
    flash(_('Ssh information deleted'))
    return redirect(url_for("ssh.provider_list"))

@bp_amazon.route('/ssh/server/add', methods=['GET', 'POST'])
@login_required
def server_add():
    form = SshServerForm()
    if form.validate_on_submit():
        ssh.add_server(form)
        flash(_('Ssh server added'))
        return redirect(url_for('deploy.deploy_list'))
    return render_template('ssh_server_add.html', form=form)

@bp_amazon.route('/ssh/server/delete/<id>')
@login_required
def server_delete(id):
    ssh.delete_server(id)
    flash(_('Ssh server deleted'))
    return redirect(url_for('deploy.deploy_list'))

@bp_amazon.route('/ssh/server/deploy/<id>')
@login_required
def server_deploy(id):
    ssh.deploy_server(id)
    flash(_('Ssh server deploy launched'))
    return redirect(url_for('deploy.deploy_list'))
