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

from flask import render_template, current_app, flash, redirect, url_for, jsonify, g, session
from flask.ext.login import login_required

from setup import deploy
from app import db
import os

from flask.ext.babel import gettext as _

from models import Servers_EC2
from forms import DeployForm

from tasks import deploy_on_cloud


@deploy.route('/deploy')
@login_required
def dep():
    servers = _get_servers()
    return render_template('deploy.html', servers=servers)

@deploy.route('/deploy/add', methods=['GET', 'POST'])
@login_required
def deploy_add():
    form = DeployForm()
    if form.validate_on_submit():
        server = Servers_EC2(form.name.data)
        server.access_key = form.access_key.data
        server.secret_key = form.secret_key.data
        server.key_name = form.key_name.data
        server.ssh_key = form.ssh_key.data

        db.session.add(server)
        db.session.commit()
        flash(_('Server added'))
        return redirect(url_for("deploy.dep"))
    return render_template('deploy_add.html', form=form)



@deploy.route('/deploy/status')
@login_required
def deploy_status():
    status = {}
    for serv in g.task:
        res = deploy_on_cloud.AsyncResult(g.task[serv].task_id)
        status.update({int(serv) : res.state})
    return jsonify(status)


@deploy.route('/deploy/del/<id>')
@login_required
def deploy_del(id):
    server = Servers_EC2.query.filter(Servers_EC2.id == id).first()

    if server:
        db.session.delete(server)
        db.session.commit()
        flash(_('Server deleted'))
    return redirect(url_for("deploy.dep"))

@deploy.route('/deploy/cloud/<id>')
@login_required
def deploy_cloud(id):
    task = deploy_on_ec2(id)
    session['task'].update({id : task})
    return redirect(url_for("deploy.dep"))


def _get_servers():
    _initdb()
    return Servers_EC2.query.order_by(Servers_EC2.name)

def _initdb():
    db.create_all(bind='servers_ec2')

def deploy_on_ec2(id):
    server_ec2 = Servers_EC2.query.filter(Servers_EC2.id == id).first()

    config = { 'access_key' : server_ec2.access_key,
               'secret_key' : server_ec2.secret_key,
               'elastics_ip' : server_ec2.elastics_ip,
               'instance_params' : server_ec2.instance_params,
               server_ec2.instance_params : { 'image_id' : server_ec2.image_id,
                                              'instance_type' : server_ec2.instance_type,
                                              'security_groups' : [server_ec2.security_groups],
                                              'key_name' : server_ec2.key_name,
                                            }
             }

    server_ec2.status = 1
    db.session.add(server_ec2)
    db.session.commit()
    task = deploy_on_cloud.apply_async((id, config, server_ec2.ssh_key))
    return task
