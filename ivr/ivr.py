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

class Ivr(object): 

    def __init__(self):
        pass

    def save(self, json):
        is_finish = False
        first_last = self.find_first_last_priority(json)
        action = first_last['action']
        target = first_last['nextstep']
        last = first_last['last']
        print '[my_ivr]'
        print 'exten = 1,1,%s' % self.application(action)
        while(is_finish == False):
            next_step = self.find_priority(json, target)
            if next_step:
                if target == last:
                    is_finish = True
                (action, target) = self.get_priority(next_step)
                print 'same = n,%s' % self.application(action)
            
    def application(self, app):
        if app == 'answer':
            return 'Answer()'
        if app == 'hangup':
            return 'Hangup()'
        return 'NoOp(\'%s\')' % app

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

        return(json['action'], target)
