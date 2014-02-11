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


from flask.ext.wtf import Form
from wtforms.fields import TextField, SubmitField
from wtforms.validators import Required

class LinesForm(Form):
    id = TextField('ID', [Required()])
    context = TextField('Context', [Required()])
    protocol = TextField('Protocol', [Required()])
    name = TextField('Name', [Required()])
    provisioning_extension = TextField('Provisioning code')
    device_slot = TextField('Device slot')