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

from flask import render_template, current_app, flash, redirect, url_for, jsonify, Blueprint, g
from flask.ext.login import login_required

from setup import deploy
from app import db
import os
import datetime, time

from flask.ext.babel import gettext as _

from forms import DeployForm, CloudProviderForm
from models import Servers_EC2, Cloud_Provider

from tasks import deploy_on_cloud, undeploy_on_cloud
from celery.task.control import revoke


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
        server.servers = form.cloud_provider.data

        db.session.add(server)
        db.session.commit()
        flash(_('Server added'))
        return redirect(url_for("deploy.dep"))
    return render_template('deploy_add.html', form=form)

@deploy.route('/deploy/provider/add', methods=['GET', 'POST'])
@login_required
def provider_add():
    form = CloudProviderForm()
    if form.validate_on_submit():
        provider = Cloud_Provider(form.name.data)
        provider.access_key = form.access_key.data
        provider.secret_key = form.secret_key.data
        provider.key_name = form.key_name.data
        provider.ssh_key = form.ssh_key.data

        db.session.add(provider)
        db.session.commit()
        flash(_('Provider added'))
        return redirect(url_for("deploy.dep"))
    return render_template('provider_add.html', form=form)


@deploy.route('/deploy/status')
@login_required
def deploy_status():
    status = {}
    server_ec2 = Servers_EC2.query.all()
    for serv in server_ec2:
        status.update({int(serv.id) : { 'status': _check_value(serv.status),
                                        'ip': _check_value(serv.address),
                                        'instance': _check_value(serv.instance_ec2),
                                        'progress' : _estimated_time_of_installation( \
                                                      serv.installed_time, "0:08:20") }
                           })
    return jsonify(status)

def _check_value(value):
    if not value:
        value = ''
    return value 

def _estimated_time_of_installation(installed_time, estimated_time):
    # TODO refactor this method !
    if not installed_time:
        return 0
    h1 = _check_value(installed_time).replace(microsecond=0)
    h2 = datetime.datetime.utcnow().replace(microsecond=0)
    time_for_installing = datetime.datetime.strptime(estimated_time, "%H:%M:%S")
    fix = datetime.datetime.strptime("0:00:00", "%H:%M:%S")
    diff_started = h2-h1

    if diff_started.days != 0:
        return 100

    time_of_installation = datetime.datetime.strptime(str(diff_started), "%H:%M:%S")
    time_begin = time_for_installing-time_of_installation
    time_fix = time_for_installing-fix
    percentage = int(100-round((100.0*time_begin.total_seconds())/time_fix.total_seconds()))
    if percentage > 100:
         return 100
    return percentage 

@deploy.route('/deploy/del/<id>')
@login_required
def deploy_del(id):
    undeploy_on_ec2(id)
    flash(_('Server deleted'))
    return redirect(url_for("deploy.dep"))

@deploy.route('/deploy/stop_task/<id>')
@login_required
def deploy_stop_task(id):
    _stop_task(id)
    flash(_('Task stopped'))
    return redirect(url_for("deploy.dep"))


@deploy.route('/deploy/cloud/<id>')
@login_required
def deploy_cloud(id):
    deploy_on_ec2(id)
    return redirect(url_for("deploy.dep"))

def _get_servers():
    _initdb()
    return Servers_EC2.query.order_by(Servers_EC2.name)

def _initdb():
    db.create_all(bind='servers_ec2')

def create_amazon_config(server_ec2):
    config = { 'access_key' : server_ec2.servers.access_key,
               'secret_key' : server_ec2.servers.secret_key,
               'elastics_ip' : server_ec2.elastics_ip,
               'instance_params' : server_ec2.instance_params,
               server_ec2.instance_params : { 'image_id' : server_ec2.image_id,
                                              'instance_type' : server_ec2.instance_type,
                                              'security_groups' : [server_ec2.servers.security_groups],
                                              'key_name' : server_ec2.servers.key_name,
                                            }
             }

    return config

def _stop_task(id):
    server_ec2 = Servers_EC2.query.filter(Servers_EC2.id == id).first()
    revoke(server_ec2.task_id, terminate=True)
    server_ec2.status = None
    server_ec2.address = None
    server_ec2.instance_ec2 = None
    server_ec2.installed_time = None
    db.session.add(server_ec2)
    db.session.commit()
    

def undeploy_on_ec2(id):
    server_ec2 = Servers_EC2.query.filter(Servers_EC2.id == id).first()

    if server_ec2.instance_ec2:
        config = create_amazon_config(server_ec2)
        inst = undeploy_on_cloud(server_ec2.instance_ec2, config)

    if server_ec2:
        db.session.delete(server_ec2)
        db.session.commit()

def deploy_on_ec2(id):
    server_ec2 = Servers_EC2.query.filter(Servers_EC2.id == id).first()
    config = create_amazon_config(server_ec2)

    user_info = {'user_id' : g.user.id, 'organisation_id' : g.user_organisation.id}

    task = deploy_on_cloud.apply_async((id, config, server_ec2.servers.ssh_key, user_info))
    server_ec2.task_id = task.task_id
    server_ec2.installed_time = datetime.datetime.utcnow()
    db.session.add(server_ec2)
    db.session.commit()
