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

import os
from app import db
from models import RegisterProviders, AssociateProviders
from flask import g
from register_class import registerclass
from tasks import deploy_on_cloud, undeploy_on_cloud
import datetime
from flask.ext.login import current_user

class Deploy(object): 

    def __init__(self):
        pass

    def setup(self, app):
        pass

    def activated(self, plugin_name):
        if plugin_name == 'deploy':
            return

        plugin = RegisterProviders.query.filter(RegisterProviders.name == plugin_name.capitalize()) \
                                        .first()

        if not hasattr(g, 'user_organisation'):
            return

        if plugin and plugin.id:
            provider_registered = AssociateProviders.query.filter(AssociateProviders.provider_id == plugin.id) \
                                                          .filter(AssociateProviders.organisation_id == current_user.organisation_id) \
                                                          .first()

            if not provider_registered:
                associate = AssociateProviders()
                associate.organisation_id = current_user.organisation_id
                associate.provider_id = plugin.id
                db.session.add(associate)
                db.session.commit()

    def deactivated(self, plugin_name):
        if plugin_name == 'deploy':
            return

        plugin = RegisterProviders.query.filter(RegisterProviders.name == plugin_name.capitalize()) \
                                        .first()

        if plugin and plugin.id:
            provider_registred = AssociateProviders.query.filter(AssociateProviders.provider_id == plugin.id) \
                                                         .filter(AssociateProviders.organisation_id == current_user.organisation_id) \
                                                         .first()
            if provider_registred:
                db.session.delete(provider_registred)
                db.session.commit()
        

    def register(self, app, info):
        self.db_bind = 'deploy_base'
        mydbplugindir = os.path.join(app.config['BASEDIR'],'app/plugins/deploy/db/deploy_servers.db')
        app.config['SQLALCHEMY_BINDS'].update({self.db_bind : 'sqlite:///%s' % mydbplugindir})

        self._register_provider(app, info)

    def get_provider(self, id):
        provider = RegisterProviders.query.filter(RegisterProviders.id == id) \
                                          .filter(AssociateProviders.organisation_id == current_user.organisation_id) \
                                          .first()
        return provider.base_url + '/server/add'

    def get_servers(self):
        servers = []
        providers = RegisterProviders.query.all()
        for provider in providers:
            cls = registerclass(provider)
            servers.append({'provider' : provider.name.lower(), 'sql' : cls.get_servers()})
        return servers

    def add_server(self, form):
        server = DeployServers(form.name.data)
        server.organisation_id = current_user.organisation_id
        db.session.add(server)
        db.session.commit()

    def delete_server(self, id):
        pass

    def deploy_server(self, provider, id):
        user_info = {'user_id' : current_user.id,
                     'organisation_id' : current_user.organisation_id
                    }
        return deploy_on_cloud.apply_async((provider, id, user_info))

    def undeploy_server(self, provider, id):
        return undeploy_on_cloud.apply_async((provider, id))

    def stop_task(self, provider, id):
        prov = RegisterProviders.query.filter(RegisterProviders.name == provider.capitalize()).first()
        cls = registerclass(prov)
        cls.stop_task(id)

    def _register_provider(self, app, info):
        with app.app_context():
            db.create_all(bind=self.db_bind)
            provider = RegisterProviders.query.filter(RegisterProviders.name == info['name']).first()
            if not provider:
                provider = RegisterProviders(info['name'])
                provider.base_url = info['base_url']
                provider.classname = info['classname']
                db.session.add(provider)
                db.session.commit()

    def get_status(self):
        status = {}
        servers = self.get_servers()
        for server in servers: 
            for serv in server['sql']:
                myid = str(server['provider']+"-"+str(serv.id))
                status.update({myid : { 'status': self._check_value(serv.status), 
                                                'ip': self._check_value(serv.address), 
                                                'instance': self._check_value(serv.instance), 
                                                'progress' : self._estimated_time_of_installation( \
                                                             serv.installed_time, "0:08:20") } 
                              })
        return status

    def _check_value(self, value): 
        if not value: 
            value = '' 
        return value  
 
    def _estimated_time_of_installation(self, installed_time, estimated_time): 
        # TODO refactor this method ! 
        if not installed_time: 
            return 0 
        h1 = self._check_value(installed_time).replace(microsecond=0) 
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
