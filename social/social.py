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

from flask.ext.couchdb import ViewDefinition, paginate
from flask.ext.login import current_user
from app.extensions import couchdbmanager
from flask import g, request, jsonify
from models import Messages

class Social(object):
    def __init__(self):
        self.all = ViewDefinition('messages', 'all',
                                  '''function(doc) {
                                         emit(doc.organisation_id, doc)
                                     }''',
                                  descending=True)
        couchdbmanager.add_viewdef(self.all)

    def add(self, content):
        message = Messages(user_id=current_user.id, \
                           organisation_id=current_user.organisation_id, \
                           displayname=current_user.displayname, \
                           content=content)
        message.store()

    def list(self):
        return paginate(self.all[current_user.organisation_id], 5, request.args.get('start'))

    def like(self, id):
        message = Messages.load(id)
        if message:
            message.like.append(user_id=current_user.id, \
                                displayname=current_user.displayname, \
                                organisation_id=current_user.organisation_id, \
                                is_like = 1)
            message.store()

    def delete(self, id):
        message = Messages.load(id)
        if message:
            message.organisation_id = None
            message.store()

    def comment(self, id):
        content=request.form['comment']
        message = Messages.load(id)
        message.comments.append(user_id=current_user.id, \
                                organisation_id=current_user.organisation_id, \
                                displayname=current_user.displayname, \
                                content=content)
        message.store()
        return jsonify({'response' : True})
