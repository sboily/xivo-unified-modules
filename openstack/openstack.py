#!/usr/bin/python

from novaclient.v1_1 import client
import time

class OpenStackConn:
    def __init__(self, config):
        self.conn = None
        self.login = config['login']
        self.password = config['password']
        self.tenant = config['tenant']
        self.api = config['api']
        self.image = config['image']
        self.flavor = config['flavor']
        self.name = config['name']
        self.keypair = config['keypair']
        self.subnet = config['subnet']

    def connect(self):
        self.conn = client.Client(self.login, self.password, self.tenant, self.api)

    def create_instance(self):
        image = self.conn.images.find(name=self.image)
        flavor = self.conn.flavors.find(name=self.flavor)
        myserver = self.conn.servers.create(self.name,image,flavor.id,key_name=self.keypair)

        while myserver.status != 'ACTIVE':
            myserver.get()
            time.sleep(1)

        ip = myserver.addresses[self.subnet][0]['addr']

        return ip
