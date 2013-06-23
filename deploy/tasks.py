from fabric.api import run, sudo, put, env
from amazon import EC2Conn
import time
import tempfile
import os
import sys
from app.extensions import celery

@celery.task(name='tasks.deploy_on_cloud', ignore_result=False)
def deploy_on_cloud(id, config, ssh_key):
    instance = create_new_instance_on_amazon(config)
    print 'Waiting for the amazon checking ...'
    time.sleep(60)
    print 'Finish !'
    deploy_xivo_on_amazon(instance,ssh_key)

def deploy_xivo_on_amazon(instance, ssh_key):

    env.host_string = "admin@%s" % (instance.ip_address)

    _, key_file = tempfile.mkstemp()
    file = open(key_file, 'w')
    file.write(ssh_key)
    file.close()

    os.chmod(key_file, 0400)

    env.key_filename = key_file
    remote_dahdi_init = '/etc/init.d/'
    dahdi_src = 'dahdi'
    xivo_configure_src = 'xivo-configure'

    # Install XiVO
    sudo('apt-get update')
    sudo('apt-get -y install curl')
    run('curl -O http://mirror.xivo.fr/fai/xivo-migration/xivo_install_skaro.sh')
    run('chmod +x xivo_install_skaro.sh')
    put(dahdi_src, remote_dahdi_init, use_sudo=True)
    sudo('chmod 755 /etc/init.d/dahdi')
    sudo('yes n | LANG=en_US.UTF-8 ./xivo_install_skaro.sh')
    put(xivo_configure_src)
    run('chmod +x xivo-configure')
    sudo('./xivo-configure')

    os.remove(key_file)


def create_new_instance_on_amazon(config):
    a = EC2Conn(config)
    a.connect()
    instance = a.create_instance()
    return instance

