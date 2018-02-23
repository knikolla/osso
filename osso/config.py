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

SAML_ENTITY_ID = 'https://kristi/idp'

KEYFILE = 'etc/ca.key'
CERTFILE = 'etc/ca.crt'

SAML_SP = {
    'https://sp.example.com/SAML2': {
        'POST': 'https://sp.example.com/SAML2/POST'
    },
    'https://sp.testshib.org/shibboleth-sp': {
        'POST': 'https://sp.testshib.org/Shibboleth.sso/SAML2/POST'
    },
    'https://sp.example.org/shibboleth': {
        'POST': 'http://128.31.25.149/Shibboleth.sso/SAML2/POST'
    }
}
