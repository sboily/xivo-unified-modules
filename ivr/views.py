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

from flask import render_template, url_for, request, jsonify, redirect, flash
from flask.ext.login import login_required
import json

from setup import bp_ivr, ivr

@bp_ivr.route('/ivr')
@login_required
def ivr_list():
    my_ivr = ivr.list()
    return render_template('ivr.html', ivr=my_ivr)

@bp_ivr.route('/ivr/add')
@login_required
def ivr_add():
    return render_template('ivr_add.html')

@bp_ivr.route('/ivr/save', methods=['POST'])
@login_required
def ivr_save():
    ivr.save(request.json)
    return jsonify({'Response' : True})

@bp_ivr.route('/ivr/edit/<id>')
@login_required
def ivr_edit(id):
    my_ivr = ivr.edit(id)
    return render_template('ivr_edit.html', name=my_ivr.name, nodes=json.loads(my_ivr.nodes), connections=json.loads(my_ivr.connections))
    #flash('Not implemented !')
    #return redirect(url_for("ivr.ivr_list"))

@bp_ivr.route('/ivr/delete/<id>')
@login_required
def ivr_del(id):
    ivr.delete(id)
    flash('Ivr deleted')
    return redirect(url_for("ivr.ivr_list"))
