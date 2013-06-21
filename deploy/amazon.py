#!/usr/bin/python

from boto.ec2.connection import EC2Connection
import sys
import time

class EC2Conn:
    def __init__(self, config):
        self.conn = None
        self.access_key = config['access_key']
        self.secret_key = config['secret_key']
        self.elastics_ip = config['elastics_ip']
        self.server_type = config
        self.instance_params = config['instance_params']

    def connect(self):
        self.conn = EC2Connection(self.access_key, self.secret_key)

    def create_instance(self):
        address = self.elastics_ip
        instance_params = self.instance_params
        reservation = self.conn.run_instances( **self.server_type[instance_params])
        print reservation
        instance = reservation.instances[0]
        time.sleep(10)
        while instance.state != 'running':
            time.sleep(5)
            instance.update()
            print "Instance state: %s" % (instance.state)

        print "instance %s done!" % (instance.id)

        if address:
            success = self.link_instance_and_ip(instance.id, address)
            if success:
                print "Linked %s to %s" % (instance.id, address)
            else:
                print "Falied to link%s to %s" % (instance.id, address)
            instance.update()

        return instance

    def link_instance_and_ip(self, instance_id, ip):
        success = self.conn.associate_address(instance_id=instance_id, public_ip=ip)
        if success:
            print "Sleeping for 60 seconds to let IP attach"
            time.sleep(60)

            return success

    def unlink_instance_and_ip(self, instance_id, ip):
        return self.conn.disassociate_address(instance_id=instance_id, public_ip=ip)

    def get_instances(self):
        return self.conn.get_all_instances()
