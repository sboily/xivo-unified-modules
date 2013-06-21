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


from flask.ext.wtf import TextField, ValidationError, SubmitField, TextAreaField
from flask.ext.wtf import Required, IPAddress, Regexp, validators
from app.utils import Form
from flask.ext.babel import lazy_gettext as _

class DeployForm(Form):
    name = TextField(_('Name'), [Required(),
        validators.Length(min=3, max=30),
        validators.Regexp(r'^[^@:]*$', message=_("Name shouldn't contain '@' or ':'"))
    ])

    address = TextField(_('Address'))
    access_key = TextField(_('Access key'))
    secret_key = TextField(_('Secret key'))
    key_name = TextField(_('Key Name'))

    ssh_key = TextAreaField(_('SSH key'))

    submit = SubmitField(_('Submit'))
