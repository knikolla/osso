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

import json
from os import path

conf_files = [f for f in ['config.json',
                          'etc/config.json',
                          '/etc/osso/config.json'] if path.isfile(f)]

if not conf_files:
    raise Exception

CONFIG = json.loads(open(conf_files[0]).read())

SAML_ENTITY_ID = CONFIG['idp_entity_id']
IDP_ROOT_URL = CONFIG['idp_root_url']

KEYFILE = CONFIG['keyfile']
CERTFILE = CONFIG['certfile']

SAML_SP = CONFIG['service_providers']
