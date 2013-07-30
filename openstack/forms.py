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


from flask.ext.wtf import TextField, SubmitField, TextAreaField, QuerySelectField
from flask.ext.wtf import Required, Regexp, validators
from flask.ext.babel import lazy_gettext as _
from flask import g
from app.utils import Form
from models import ProviderOpenStack

def get_configurations():
    return ProviderOpenStack.query.filter(ProviderOpenStack.organisation_id == g.user_organisation.id) \
                               .all()

class OpenStackForm(Form):
    name = TextField(_('Name'), [Required(),
        validators.Length(min=3, max=30),
        validators.Regexp(r'^[^@:]*$', message=_("Name shouldn't contain '@' or ':'"))
    ])

    login = TextField(_('Login'))
    password = TextField(_('Password'))
    tenant = TextField(_('Tenant name'))
    api_url = TextField(_('API url'))
    image_name = TextField(_('Image name'))
    flavor = TextField(_('Flavor'))
    subnet_name = TextField(_('Subnet Name'))
    keypair_name = TextField(_('Key Name'))
    keypair_private = TextAreaField(_('SSH key'))

    submit = SubmitField(_('Submit'))

class OpenStackServerForm(Form):
    name = TextField(_('Name'), [Required(),
        validators.Length(min=3, max=30),
        validators.Regexp(r'^[^@:]*$', message=_("Name shouldn't contain '@' or ':'"))
    ])

    configuration = QuerySelectField(_('OpenStack configuration'), [Required()], get_label='name', \
                                       query_factory=get_configurations, \
                                       allow_blank=True, blank_text=_('Please choose a configuration ...'))

    submit = SubmitField(_('Submit'))
