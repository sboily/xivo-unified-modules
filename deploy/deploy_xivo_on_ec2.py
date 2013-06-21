#!/usr/bin/python

from fabric.api import run, sudo, put, env
from amazon import EC2Conn
import time
from extensions import db
from models import Servers_EC2

def deploy_xivo_on_amazon():

    instance = create_new_instance_on_amazon()

    env.host_string = "admin@%s" % (instance.ip_address)
    env.key_filename = SSH_KEY
    remote_dahdi_init = '/etc/init.d/'

    # Install XiVO
    sudo('apt-get update')
    sudo('apt-get -y install curl')
    run('curl -O http://mirror.xivo.fr/fai/xivo-migration/xivo_install_skaro.sh')
    run('chmod +x xivo_install_skaro.sh')
    put('dahdi', remote_dahdi_init, use_sudo=True)
    sudo('chmod 755 /etc/init.d/dahdi')
    sudo('yes n | LANG=en_US.UTF-8 ./xivo_install_skaro.sh')


def create_new_instance_on_amazon():
    a = EC2Conn(ACCESS_KEY,SECRET_KEY,ELASTICS_IP,SERVER_TYPES, INSTANCE_PARAMS)
    a.connect()
    instance = a.create_instance()
    print 'Waiting for the amazon checking ...'
    time.sleep(60)
    return instance

SQLALCHEMY_BINDS.append({'servers_ec2':
                         'sqlite:////servers_ec2.db'
                        })

db.create_all(bind=['servers_ec2'])
server_ec2 = Servers_EC2('xivo')
db.session.add(server_ec2)
db.session.commit()

ACCESS_KEY = server_ec2.access_key
SECRET_KEY = server_ec2.secret_key
ELASTICS_IP = server_ec2.elastics_ip
INSTANCE_PARAMS = server_ec2.instance_params

MAIN_SG = server_ec2.key_name
MAIN_KP = server_ec2.security_groups

SSH_KEY = server_ec2.ssh_keys

SERVER_TYPES = { server_ec2.params : {'image_id' : server_ec2.image_id,
                          'instance_type' : server_ec2.instance_type,
                          'security_groups' : [MAIN_SG],
                          'key_name' : MAIN_KP,
                         },
                }


#deploy_xivo_on_amazon()

