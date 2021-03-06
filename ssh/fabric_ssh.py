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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.# -*- coding: utf-8 -*-

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

from fabric.api import run, sudo, put, env
import tempfile
import os


def deploy_xivo_on_ssh(login, password, ip):

    env.host_string = "%s@%s" % (login, ip)
    env.password = password

    basedir = os.path.abspath(os.path.dirname(__file__))
    remote_dahdi_init = '/etc/init.d/'
    dahdi_src = os.path.join(basedir, '../deploy/dahdi')
    xivo_configure_src = os.path.join(basedir, '../deploy/xivo-configure')
    webservice_sql_src = os.path.join(basedir, '../deploy/webservices.sql')


    # Install XiVO
    run('apt-get update')
    run('apt-get -y install curl')
    run('apt-get -y install sudo')
    run('curl -O http://mirror.xivo.fr/fai/xivo-migration/xivo_install_skaro.sh')
    run('chmod +x xivo_install_skaro.sh')
    put(dahdi_src, remote_dahdi_init, use_sudo=True)
    run('echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen')
    run('locale-gen')
    run('chmod 755 /etc/init.d/dahdi')
    run('yes n | LANG=en_US.UTF-8 ./xivo_install_skaro.sh')
    put(xivo_configure_src)
    run('chmod +x xivo-configure')
    run('./xivo-configure')
    put(webservice_sql_src, '/tmp')
    run('sudo -u postgres psql -f /tmp/webservices.sql')
