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
import os
import json

class Ivr(object): 

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
        my_ivr = IvrDB.query.filter(IvrDB.name == name) \
                            .first()

        if not my_ivr:
            my_ivr = IvrDB(name)

        my_ivr.nodes = json.dumps(result['blocks'])
        my_ivr.connections = json.dumps(result['connections'])

        db.session.add(my_ivr)
        db.session.commit()

    def list(self):
        return IvrDB.query.order_by(IvrDB.name) 

    def delete(self, id):
        my_ivr = IvrDB.query \
                      .filter(IvrDB.id == id) \
                      .first()
        if my_ivr:
            db.session.delete(my_ivr)
            db.session.commit()

    def edit(self, id):
        my_ivr = IvrDB.query.filter(IvrDB.id == id) \
                            .first()
        return my_ivr

    def show(self):
        return True
        is_finish = False
        first_last = self.find_first_last_priority(json)
        action = first_last['action']
        target = first_last['nextstep']
        last = first_last['last']
        config = first_last['config']
        print '[my_ivr]'
        print 'exten = s,1,%s' % self.application(action, config)
        while(is_finish == False):
            next_step = self.find_priority(json, target)
            if next_step:
                if target == last:
                    is_finish = True
                (action, target, config) = self.get_priority(next_step)
                print 'same = n,%s' % self.application(action, config)
            
    def application(self, app, config):
        if app == 'answer':
            return 'Answer()'
        if app == 'hangup':
            return 'Hangup()'
        if app == 'prompts':
            app_config = 'Playback(%s)' % config['prompt_path']
            return app_config
        if app == 'execute':
            app_config = '%s(%s)' %(config['application'], config['arguments'])
            return app_config
        return 'NoOp(\'%s\')' % app

    def set_application_config(self, app, config):
        print app
        print config

    def find_first_last_priority(self, json):
        first_and_last = {}
        for j in json:
            if json[j].has_key('source_sourceid') and not json[j].has_key('target_sourceid'):
                if json[j]['source_sourceid'] == json[j]['id']:
                    first_and_last.update({'action' : json[j]['action']})
                    first_and_last.update({'nextstep' : json[j]['source_targetid']})
            if json[j].has_key('target_sourceid') and not json[j].has_key('source_sourceid') :
                if json[j]['target_targetid'] == json[j]['id']:
                    first_and_last.update({'last' : json[j]['target_targetid']})
            if json.has_key('config'):
                first_and_last.update({'config' : json[j]['config']})
            else:
                first_and_last.update({'config' : ''})

        return first_and_last

    def find_priority(self, json, target):
        for j in json:
            if json[j]['id'] == target:
                return(json[j])
        return False

    def get_priority(self, json):
        if json.has_key('source_targetid'):
            target = json['source_targetid']
        else:
            target = json['target_sourceid']

        if json.has_key('config'):
            config = json['config']
        else:
            config = ''

        return(json['action'], target, config)
