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

from yapsy.IPlugin import IPlugin
from setup import bp_amazon
from deploy_amazon import DeployOnAmazon
import views

class DeployAmazonPlugin(IPlugin):

    def setup(self, app):
        app.register_blueprint(bp_amazon)

        deploy_amazon = DeployOnAmazon()
        deploy_amazon.setup(app)

    def plugin_endpoint(self):
        return "amazon.provider_list"
