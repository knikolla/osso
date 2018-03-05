#    osso
#    Copyright (C) 2018  Mass Open Cloud
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

from osso import config

CONFIG = config.CONFIG

PRIVATE = None
PUBLIC = None
CERT = None


class Key(object):
    def __init__(self, path):
        with open(path) as f:
            self.full_key = f.read()
        self.key = self.strip(self.full_key)

    @staticmethod
    def strip(full_key):
        key = full_key.replace('-----BEGIN RSA PRIVATE KEY-----\n', '')
        key = key.replace('\n-----END RSA PRIVATE KEY-----\n', '')
        key = key.replace('-----BEGIN CERTIFICATE-----\n', '')
        key = key.replace('\n-----END CERTIFICATE-----\n', '')
        key = key.replace('-----BEGIN PUBLIC KEY-----\n', '')
        key = key.replace('\n-----END PUBLIC KEY-----\n', '')
        return key

    @property
    def key_oneline(self):
        return self.key.replace('\n', '')


def load_keys():
    global PRIVATE, PUBLIC, CERT
    PRIVATE = Key(CONFIG['private_key'])
    PUBLIC = Key(CONFIG['public_key'])
    CERT = Key(CONFIG['cert'])


load_keys()
