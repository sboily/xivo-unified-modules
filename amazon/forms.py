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
from models import ProviderAmazon

def get_configurations():
    return ProviderAmazon.query.filter(ProviderAmazon.organisation_id == current_user.organisation_id) \
                               .all()

class AmazonForm(Form):
    name = TextField(_('Name'), [Required(),
        Length(min=3, max=30),
        Regexp(r'^[^@:]*$', message=_("Name shouldn't contain '@' or ':'"))
    ])

    access_key = TextField(_('Access key'))
    secret_key = TextField(_('Secret key'))
    key_name = TextField(_('Key Name'))

    ssh_key = TextAreaField(_('SSH key'))

    submit = SubmitField(_('Submit'))

class AmazonServerForm(Form):
    name = TextField(_('Name'), [Required(),
        Length(min=3, max=30),
        Regexp(r'^[^@:]*$', message=_("Name shouldn't contain '@' or ':'"))
    ])

    configuration = QuerySelectField(_('Amazon configuration'), [Required()], get_label='name', \
                                       query_factory=get_configurations, \
                                       allow_blank=True, blank_text=_('Please choose a configuration ...'))

    submit = SubmitField(_('Submit'))
