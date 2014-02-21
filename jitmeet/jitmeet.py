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

from flask.ext.login import current_user
from flask.ext.mail import Message
from flask import request
from app.extensions import db, mail
from models import RoomDB
import os

class JitMeet(object):

    def setup(self, app):
        self.db_bind = 'jitmeet'
        mydbplugindir = os.path.join(app.config['BASEDIR'],'app/plugins/jitmeet/db/jitmeet.db')
        app.config['SQLALCHEMY_BINDS'].update({self.db_bind : 'sqlite:///%s' % mydbplugindir})

        with app.app_context():
            db.create_all(bind=self.db_bind)

    def add(self, form):
        name = form.name.data
        pin = form.pin.data
        start_time = form.start_time.data
        end_time = form.end_time.data

        room = RoomDB(name=name)
        room.organisation_id = current_user.organisation_id
        room.hash = os.urandom(16).encode('hex')
        room.organized_by = current_user.displayname

        if pin:
            room.pin = pin

        if start_time:
           room.start_time = start_time

        if end_time:
           room.end_time = end_time

        db.session.add(room)
        db.session.commit()

    def edit(self, form, id):
        room = RoomDB.query.filter_by(id=id).first()
        if form.validate_on_submit():
            form.populate_obj(room)
            db.session.add(room)
            db.session.commit()
            return True

        return False

    def get(self, id):
        return RoomDB.query.filter_by(id=id).first()

    def list(self):
        return RoomDB.query.filter(RoomDB.organisation_id == current_user.organisation_id) \
                           .order_by(RoomDB.name)

    def delete(self, id):
        room = RoomDB.query \
                     .filter(RoomDB.id == id) \
                     .filter(RoomDB.organisation_id == current_user.organisation_id) \
                     .first()
        if room:
            db.session.delete(room)
            db.session.commit()

    def send_invite(self, form, url):
        recipients = form['email'].split(";")
        body="Hello !\r\n\r\nYou are invited to partipate to this videoconferencing, please click on this link (only working with the latest chrome browser)\r\n%s" % url
        msg = Message(subject="Video conf invitation",
                      body=body,
                      sender="xivo-cloud@xivo.fr",
                      recipients=recipients)

        mail.send(msg)
