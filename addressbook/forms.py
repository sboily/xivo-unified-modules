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


from wtforms.fields import TextField, BooleanField, PasswordField, RadioField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import ValidationError, Required, Length, Regexp, EqualTo, Email
from flask.ext.babel import lazy_gettext as _
from app.utils import Form

class AddressBookForm(Form):
    username = TextField(_('Username'), [Length(min=3, max=20),
                                         Regexp(r'^[^@:]*$', message=_("Username shouldn't contain '@' or ':'"))
                                        ])
    email = EmailField(_('Email address'), [
        Length(min=3, max=128),
        Email(message=_("This should be a valid email address."))
    ])
    password = PasswordField(_('Password'), [Required(),
        Length(min=8, message=_("It's probably best if your password is longer than 8 characters."))
    ])

    displayname = TextField(_('Display name'))
    organisation = TextField(_('Organisation'))
    birthday = TextField(_('Birthday'))
    gender = RadioField(_('Gender'), choices=[('M', 'Male'),('F', 'Female')])
    internal_number = TextField(_('Internal number'))
    phonenumber = TextField(_('Phone number'))
    mobile = TextField(_('Mobile'))
    city = TextField(_('City'))
    submit = SubmitField(_('Save'))

class AddressBookServerLdapForm(Form):
    name = TextField(_('Name'), [Required()])
    host = TextField(_('LDAP host'), [Required()])
    basedn = TextField(_('Base DN'), [Required()])
    searchfilter = TextField(_('Search filter'), [Required()])
    login = TextField(_('Admin DN'))
    secret = TextField(_('Secret'))
    submit = SubmitField(_('Save'))
