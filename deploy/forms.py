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


from flask.ext.wtf import QuerySelectField, Required
from app.utils import Form
from flask import g
from flask.ext.babel import lazy_gettext as _
from models import RegisterProviders, AssociateProviders

def get_providers():
    return RegisterProviders.query.filter(AssociateProviders.organisation_id==g.user_organisation.id) \
                                  .order_by(RegisterProviders.name)


class DeployForm(Form):
    cloud_provider = QuerySelectField(_('Cloud provider'), [Required()], get_label='name', \
                                       query_factory=get_providers, \
                                       allow_blank=True, blank_text=_('Please choose a provider ...'))
