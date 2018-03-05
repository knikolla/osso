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

import base64
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import zlib
import uuid

from osso import config
from osso import saml_exceptions
from osso import pki
from osso import server

import signxml


SIGNATURE_ALGORITHM = 'rsa-sha256'
DIGEST_ALGORITHM = 'sha256'
C14N_ALGORITHM = 'http://www.w3.org/TR/2001/REC-xml-c14n-20010315'

NAMESPACES = {
    'saml': 'urn:oasis:names:tc:SAML:2.0:assertion',
    'samlp': 'urn:oasis:names:tc:SAML:2.0:protocol',
    'ds': 'http://www.w3.org/2000/09/xmldsig#',
    'md': 'urn:oasis:names:tc:SAML:2.0:metadata',
    'xs': "http://www.w3.org/2001/XMLSchema",
    'xsi': "http://www.w3.org/2001/XMLSchema-instance"
}

for k, v in NAMESPACES.items():
    ET.register_namespace(k, v)


def decode_saml_request(request):
    return zlib.decompress(base64.b64decode(request), -15).decode('utf-8')


class AuthenticationRequest(object):
    # SAMPLE AUTHN REQUEST
    # <samlp:AuthnRequest
    #      xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
    #      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"
    #      ID="identifier_1"
    #      Version="2.0"
    #      IssueInstant="2004-12-05T09:21:59Z"
    #      AssertionConsumerServiceIndex="1">
    #       <saml:Issuer>https://sp.example.com/SAML2</saml:Issuer>
    #       <samlp:NameIDPolicy
    #          AllowCreate="true"
    #          Format="urn:oasis:names:tc:SAML:2.0:nameid-format:transient"/>
    # </samlp:AuthnRequest>

    # As per xmlns, sampl:AuthnRequest is expanded to the below
    ROOT_TAG = '{urn:oasis:names:tc:SAML:2.0:protocol}AuthnRequest'
    NAMEID_TAG = '{urn:oasis:names:tc:SAML:2.0:protocol}NameIDPolicy'
    ISSUER_TAG = '{urn:oasis:names:tc:SAML:2.0:assertion}Issuer'

    def __init__(self, string):
        self.root = self.parse_root(string)
        self.id = self.parse_id()
        self.time_issued = self.parse_timestamp()
        self.nameid_policy = self.parse_nameid_policy()
        self.issuer = self.parse_issuer()

    def parse_root(self, string):
        root = ET.fromstring(string)
        if (
                root.tag != self.ROOT_TAG or
                root.attrib['Version'] != '2.0'
        ):
            raise saml_exceptions.InvalidAuthRequest
        return root

    def parse_timestamp(self):
        date_str = "%Y-%m-%dT%H:%M:%SZ"
        time_issued = datetime.strptime(self.root.attrib['IssueInstant'],
                                        date_str)
        return time_issued

    def parse_issuer(self):
        issuer = self.root.find(self.ISSUER_TAG).text
        if issuer not in config.SAML_SP:
            raise saml_exceptions.InvalidAuthRequest
        return issuer

    def parse_id(self):
        return self.root.attrib['ID']

    def parse_nameid_policy(self):
        return self.root.find(self.NAMEID_TAG).attrib.get('Format')


class AuthenticationResponse(object):
    def __init__(self, username, first_name, last_name, email,
                 sp, in_response_to):
        endpoint = config.SAML_SP[sp]['bindings']['POST']
        timestamp = datetime.utcnow()
        valid_until = timestamp + timedelta(hours=1)
        response_id = '_' + uuid.uuid4().hex
        assertion_id = '_' + uuid.uuid4().hex
        response = server.render_template(
            'saml_assertion.xml',
            issuer=config.IDP_ENTITY_ID,
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            sp=sp,
            assertion_id=assertion_id,
            response_id=response_id,
            in_response_to=in_response_to,
            endpoint=endpoint,
            timestamp=timestamp.isoformat(),
            valid_until=valid_until.isoformat()
        )
        self.root = ET.fromstring(response)
        self.root = self.sign(self.root, assertion_id)

    @staticmethod
    def sign(root, uri):
        return signxml.XMLSigner(
            signature_algorithm=SIGNATURE_ALGORITHM,
            digest_algorithm=DIGEST_ALGORITHM,
            c14n_algorithm=C14N_ALGORITHM
        ).sign(
            root,
            cert=pki.CERT.key,
            key=pki.PRIVATE.key,
            reference_uri=uri
        )

    def assertion_root(self):
        return self.root.find('saml:Assertion', NAMESPACES)

    def encoded(self):
        return base64.b64encode(self.to_string())

    def to_string(self):
        return ET.tostring(self.root, encoding='utf8', method='xml')


def get_metadata(root_url):
    return server.render_template(
        'saml_metadata.xml',
        entity_id=config.IDP_ENTITY_ID,
        certificate=pki.CERT.full_key,
        root_url=root_url,
        valid_until=(datetime.utcnow() + timedelta(days=7)).isoformat()
    )
