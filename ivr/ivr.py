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

from app import db
from models import IvrDB
from flask import g
import os
import json

class Ivr(object):

    nodes = None
    connections = None
    dialplan = None

    def __init__(self):
        pass

    def setup(self, app):
        self.db_bind = 'ivr'
        mydbplugindir = os.path.join(app.config['BASEDIR'],'app/plugins/ivr/db/ivr.db')
        app.config['SQLALCHEMY_BINDS'].update({self.db_bind : 'sqlite:///%s' % mydbplugindir})

        with app.app_context():
            db.create_all(bind=self.db_bind)

    def save(self, result):
        name = result['name']
        is_edit = result['is_edit']
        old_name = False
        if result.has_key('old_name'):
            query_name = result['old_name']
            old_name = True
        else:
            query_name = name

        my_ivr = IvrDB.query.filter(IvrDB.name == query_name) \
                            .filter(IvrDB.server_id == g.server_id) \
                            .filter(IvrDB.organisation_id == g.user_organisation.id) \
                            .first()

        if is_edit:
            info = "edit"
        else:
            info = "add"
            my_ivr = IvrDB(name)

        if old_name:
            my_ivr.name = name
        my_ivr.nodes = json.dumps(result['nodes'])
        my_ivr.connections = json.dumps(result['connections'])
        my_ivr.organisation_id = g.user_organisation.id
        my_ivr.server_id = g.server_id

        db.session.add(my_ivr)
        db.session.commit()

        return { 'action' : info, 'id' : my_ivr.id }

    def list(self):
        return IvrDB.query.filter(IvrDB.organisation_id == g.user_organisation.id) \
                          .filter(IvrDB.server_id == g.server_id) \
                          .order_by(IvrDB.name) 

    def delete(self, id):
        my_ivr = IvrDB.query \
                      .filter(IvrDB.id == id) \
                            .filter(IvrDB.server_id == g.server_id) \
                      .filter(IvrDB.organisation_id == g.user_organisation.id) \
                      .first()
        if my_ivr:
            db.session.delete(my_ivr)
            db.session.commit()

    def edit(self, id):
        my_ivr = IvrDB.query.filter(IvrDB.id == id) \
                            .filter(IvrDB.server_id == g.server_id) \
                            .filter(IvrDB.organisation_id == g.user_organisation.id) \
                            .first()
        return my_ivr

    def debug(self, my_ivr):
        import pprint
        pprint.pprint(json.loads(my_ivr.nodes))
        pprint.pprint(json.loads(my_ivr.connections))


    def shows(self, server_id):
        my_ivr = IvrDB.query.filter(IvrDB.organisation_id == g.user_organisation.id) \
                            .filter(IvrDB.server_id == server_id) \
                            .all()

        ivrs = '; Produce by XiVO cloud IVR<br>'
        for ivr in my_ivr:
            ivrs += self.show(ivr.id, server_id)

        return ivrs

    def show(self, id, server_id=None):
        global nodes
        global connections
        global dialplan

        if server_id == None:
            server_id = g.server_id

        my_ivr = IvrDB.query.filter(IvrDB.id == id) \
                            .filter(IvrDB.server_id == server_id) \
                            .filter(IvrDB.organisation_id == g.user_organisation.id) \
                            .first()

        nodes = json.loads(my_ivr.nodes)
        connections = json.loads(my_ivr.connections)
        dialplan = []

        dialplan.append("[myivr-%s]" % my_ivr.name)

        my_start = self.start()
        start = "exten = %s,1,NoOp(IVR %s launched with extension %s)" \
                     %(my_start['extension'], my_ivr.name, my_start['extension'])
        dialplan.append({my_start['extension'] : [start]})

        target = my_start['target']
        self.generate_same(target, my_start['extension'])

        d = self.generate_dialplan()
        return '<br>'.join(d)

    def generate_dialplan(self):
        final_dialplan = []
        final_dialplan.append(dialplan[0])
        for d in sorted(dialplan[1].keys()):
            for e in dialplan[1][d]:
                final_dialplan.append(e)
            final_dialplan.append('<br>')
        return final_dialplan


    def generate_same(self, target, exten):
        while True:
            my_app = self.get_application(target)

            if my_app:
                for d in my_app:
                    dialplan[1][exten].append("same = n,%s" % d)

            target = self.get_next_priority(target)
            if not target:
                break

        return dialplan


    def get_application(self, target):
        for node in nodes:
            if node['id'] == target:
                if node.has_key('config'):
                    config = node['config']
                else:
                    config = None
                return self.application(node['id'], node['action'], config)

    def get_next_priority(self, id):
        target = {}
        return self.find_connection(id)

    def start(self):
        my_start = {}
        for node in nodes:
            if node['action'] == 'start':
                my_start.update({'id': node['id']})
                my_start.update({'target': self.find_connection(node['id'])})
                extension = 's'
                if node.has_key('config'):
                    if node['config'].has_key('extension') and node['config']['extension'] != '':
                        extension = node['config']['extension']
                my_start.update({'extension': extension})
                return my_start
        return False

    def find_connection(self, id):
        for conn in connections:
            if conn['sourceId'] == id and not conn['digitId']:
                return conn['targetId']
        return False

    def application(self, id, app, config):
        app_config = []
        if app == 'answer':
            return ['Answer()']
        if app == 'hangup':
            return ['Hangup()']
        if app == 'prompts':
            app_config = ['Playback(%s)' % self.application_config(config, 'prompt_path')]
            return app_config
        if app == 'execute':
            app_config = ['%s(%s)' %(self.application_config(config, 'application'), \
                                    self.application_config(config, 'arguments'))]
            return app_config
        if app == 'wait4digits':
            conf = self.application_config(config, 'wait_prompt_path')
            if conf != 'error':
                app_config.append('Background(%s)' % conf)
                app_config.append('WaitExten(3)')
            else:
                app_config = ['WaitExten()']

            branch = self.application_find_digits(id)
            for exten in branch:
                dialplan[1].update({exten['extension'] : ["exten = %s,1,NoOp(You have pressed %s)" %(exten['extension'], exten['extension'])]})
                self.generate_same(exten['target'], exten['extension'])

            return app_config
        if app == 'voicemail':
            return ['Voicemail(%s)' % self.application_config(config, 'mailbox'), 'Hangup()']
        if app == 'debug':
            return ['NoOp(%s)' % self.application_config(config, 'arguments')]
        if app == 'func':
            return ['NoOp(func is not supported for the moment)']
        if app == 'language':
            return ['Set(CHANNEL(language)=%s)' % self.application_config(config, 'language')]
        if app == 'authenticate':
            return ['Authenticate(%s,,%s)' %(self.application_config(config, 'code'), self.application_config(config, 'maxdigits'))]
        if app == 'switchivr':
            return ['Goto(myivr-%s,%s,1)' %(self.application_config(config, 'name'), self.application_config(config, 'start'))]
        return ['NoOp(\'%s\')' % app]

    def application_find_digits(self, id):
        digits = []
        for conn in connections:
            if conn['sourceId'] == id and conn['digitId']:
                digits.append({'extension' : conn['digitId'], 'target' : conn['targetId']})
        return digits

    def application_config(self, config, path):
        if not config:
            return 'error'

        if config.has_key(path):
             return config[path]

        return 'error'
