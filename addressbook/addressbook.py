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

import ldap

class AddressBook(object):

    def __init__(self):
        self.basedn = ""
        self.admindn = ""
        self.secret = ""
        self.searchscope = ldap.SCOPE_SUBTREE
        self.host = ""

    def connect(self):
        try:
            conn = ldap.open(self.host)
            conn.protocol_version = ldap.VERSION3
            return conn
        except ldap.LDAPError, e:
            print e

    def list(self):
        retrieveAttributes = ['givenName', 'sn', 'telephoneNumber', 'roomNumber']
        searchFilter = "cn=*"
        results = []
        conn = self.connect()
        try:
            ldap_result_id = conn.search(self.basedn, self.searchscope, searchFilter, retrieveAttributes)
            while 1:
                result_type, result_data = conn.result(ldap_result_id, 0)
                if (result_data == []):
                    break
                else:
                    if result_type == ldap.RES_SEARCH_ENTRY: 
                        contact = { 'uid' : str(result_data[0][0]).encode('base64','strict'),
                                    'givenname' : self.set_info_from_ldap(result_data[0][1], 'givenName', 1),
                                    'sn' : self.set_info_from_ldap(result_data[0][1], 'sn', 1),
                                    'phonenumber' : self.set_info_from_ldap(result_data[0][1], 'telephoneNumber', 1),
                                    'internalphone' : self.set_info_from_ldap(result_data[0][1], 'roomNumber', 1)
                                  }
                        results.append(contact)
        except ldap.LDAPError, e:
            print e

        return results

    def show(self, uid):
        uid = uid.decode('base64','strict')
        conn = self.connect()
        contact = conn.search(uid, self.searchscope)
        res_contact = conn.result(contact, 0)

        if res_contact:
            contact = { 'id' : str(res_contact[1][0][0]).encode('base64','strict'),
                        'username' : self.set_info_from_ldap(res_contact[1][0][1], 'uid', 1),
                        'photo' : self.set_info_from_ldap(res_contact[1][0][1], 'jpegPhoto'),
                        'displayname' : self.set_info_from_ldap(res_contact[1][0][1], 'cn', 1),
                        'birthday' : self.set_info_from_ldap(res_contact[1][0][1], 'dateOfBirth', 1),
                        'organisation' : self.set_info_from_ldap(res_contact[1][0][1], 'o', 1),
                        'lastname' : self.set_info_from_ldap(res_contact[1][0][1], 'sn', 1),
                        'firstname' : self.set_info_from_ldap(res_contact[1][0][1], 'givenName', 1),
                        'internal_number' : self.set_info_from_ldap(res_contact[1][0][1], 'roomNumber', 1),
                        'gender' : self.set_info_from_ldap(res_contact[1][0][1], 'gender', 1),
                        'email' : self.set_info_from_ldap(res_contact[1][0][1], 'mail', 1),
                        'mobile' : self.set_info_from_ldap(res_contact[1][0][1], 'mobile', 1),
                        'phonenumber' : self.set_info_from_ldap(res_contact[1][0][1], 'telephoneNumber', 1),
                        'city' : self.set_info_from_ldap(res_contact[1][0][1], 'l', 1)
                      }

            return contact

        return False

    def get_image(self, uid):
        uid = uid.decode('base64','strict')
        conn = self.connect()
        contact = conn.search(uid, self.searchscope)
        res_contact = conn.result(contact, 0)

        if res_contact:
            return self.set_info_from_ldap(res_contact[1][0][1], 'jpegPhoto')
    

    def set_info_from_ldap(self, info, field, conv=False):
        if info.has_key(field):
            if conv:
                return unicode(info[field][0],  "UTF-8")
            else:
                return info[field][0]
