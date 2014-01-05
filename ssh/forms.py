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

from wtforms.fields import TextField, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required, Regexp, Length
from flask.ext.babel import lazy_gettext as _
from flask.ext.login import current_user
from flask import g
from app.utils import Form
from models import ProviderSsh

def get_configurations():
    return ProviderSsh.query.filter(ProviderSsh.organisation_id == current_user.organisation_id) \
                               .all()

class SshForm(Form):
    name = TextField(_('Name'), [Required(),
        Length(min=3, max=30),
        Regexp(r'^[^@:]*$', message=_("Name shouldn't contain '@' or ':'"))
    ])

    login = TextField(_('Login'))
    password = TextField(_('Password'))
    ip = TextField(_('Ip'))

    submit = SubmitField(_('Submit'))

class SshServerForm(Form):
    name = TextField(_('Name'), [Required(),
        Length(min=3, max=30),
        Regexp(r'^[^@:]*$', message=_("Name shouldn't contain '@' or ':'"))
    ])

    configuration = QuerySelectField(_('Ssh configuration'), [Required()], get_label='name', \
                                       query_factory=get_configurations, \
                                       allow_blank=True, blank_text=_('Please choose a configuration ...'))

    submit = SubmitField(_('Submit'))
