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
from setup import bp_amazon, amazon
from forms import AmazonForm, AmazonServerForm

@bp_amazon.route('/amazon')
@login_required
def provider_list():
    list = amazon.get_configurations()
    return render_template('amazon_provider_list.html', list=list)

@bp_amazon.route('/amazon/add', methods=['GET', 'POST'])
@login_required
def provider_add():
    form = AmazonForm()
    if form.validate_on_submit():
        amazon.add_provider(form)
        flash(_('Amazon informations added'))
        return redirect(url_for("amazon.provider_list"))
    return render_template('amazon_provider_add.html', form=form)

@bp_amazon.route('/amazon/edit/<id>', methods=['GET', 'POST'])
@login_required
def provider_edit(id):
    provider = amazon.get_provider(id)
    form = AmazonForm(obj=provider)
    if form.validate_on_submit():
        amazon.edit_provider(form, provider)
        flash(_('Amazon provider edit'))
        return redirect(url_for("amazon.provider_list"))
    return render_template('amazon_provider_edit.html', form=form)

@bp_amazon.route('/amazon/del/<id>')
@login_required
def provider_delete(id):
    amazon.delete_provider(id)
    flash(_('Amazon information deleted'))
    return redirect(url_for("amazon.provider_list"))

@bp_amazon.route('/amazon/server/add', methods=['GET', 'POST'])
@login_required
def server_add():
    form = AmazonServerForm()
    if form.validate_on_submit():
        amazon.add_server(form)
        flash(_('Amazon server added'))
        return redirect(url_for('deploy.deploy_list'))
    return render_template('amazon_server_add.html', form=form)

@bp_amazon.route('/amazon/server/delete/<id>')
@login_required
def server_delete(id):
    amazon.delete_server(id)
    flash(_('Amazon server deleted'))
    return redirect(url_for('deploy.deploy_list'))

@bp_amazon.route('/amazon/server/deploy/<id>')
@login_required
def server_deploy(id):
    amazon.deploy_server(id)
    flash(_('Amazon server deploy launched'))
    return redirect(url_for('deploy.deploy_list'))
