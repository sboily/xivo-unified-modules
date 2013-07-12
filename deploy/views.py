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

from flask import render_template, flash, redirect, url_for, jsonify
from flask.ext.login import login_required
from setup import bp_deploy, deploy
from flask.ext.babel import gettext as _
from forms import DeployForm

@bp_deploy.route('/deploy')
@login_required
def deploy_list():
    list = deploy.get_servers()
    return render_template('deploy_list.html', list=list)

@bp_deploy.route('/deploy/add', methods=['GET', 'POST'])
@login_required
def deploy_add():
    form = DeployForm()
    if form.validate_on_submit():
        deploy.add_server(form)
        flash(_('Server added'))
        return redirect(url_for("deploy.deploy_list"))
    return render_template('deploy_add.html', form=form)

@bp_deploy.route('/deploy/del/<id>')
@login_required
def deploy_delete(id):
    servers.delete_server(id)
    flash(_('Server deleted'))
    return redirect(url_for("deploy.deploy_list"))

@bp_deploy.route('/deploy/provider/<id>')
@login_required
def deploy_get_provider(id):
    provider = {'url' : deploy.get_provider(id)}
    return jsonify(provider)

@bp_deploy.route('/deploy/status')
@login_required
def deploy_status():
    return jsonify(deploy.get_status())

@bp_deploy.route('/deploy/cloud/<provider>/<id>')
@login_required
def deploy_cloud(provider, id):
    deploy.deploy_server(provider,id)
    return redirect(url_for("deploy.deploy_list"))


@bp_deploy.route('/deploy/stop_task/<provider>/<id>')
@login_required
def deploy_stop_task(provider, id):
    deploy.stop_task(provider, id)
    flash(_('Task stopped'))
    return redirect(url_for("deploy.deploy_list"))
