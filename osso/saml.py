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

from datetime import datetime
import xml.etree.ElementTree as ET

from osso import config
from osso import saml_exceptions

# TODO(knikolla): User namespaces for cleaner tags

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
        time_now = datetime.now()
        # TODO(knikolla): Compare time
        return time_issued

    def parse_issuer(self):
        issuer = self.root.find(self.ISSUER_TAG).text
        if not issuer in config.SERVICE_PROVIDERS:
            raise saml_exceptions.InvalidAuthRequest
        return issuer

    def parse_nameid_policy(self):
        return self.root.find(self.NAMEID_TAG).attrib.get('Format')


class AuthenticationResponse(object):
    SAMPLE_RESPONSE = """<samlp:Response
        xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
        xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"
        ID="identifier_2"
        InResponseTo="identifier_1"
        Version="2.0"
        IssueInstant="2004-12-05T09:22:05Z"
        Destination="https://sp.example.com/SAML2/SSO/POST">
        <saml:Issuer>https://idp.example.org/SAML2</saml:Issuer>
        <samlp:Status>
          <samlp:StatusCode
            Value="urn:oasis:names:tc:SAML:2.0:status:Success"/>
        </samlp:Status>
        <saml:Assertion
          xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"
          ID="identifier_3"
          Version="2.0"
          IssueInstant="2004-12-05T09:22:05Z">
          <saml:Issuer>https://idp.example.org/SAML2</saml:Issuer>
          <!-- a POSTed assertion MUST be signed -->
          <ds:Signature
            xmlns:ds="http://www.w3.org/2000/09/xmldsig#">...</ds:Signature>
          <saml:Subject>
            <saml:NameID
              Format="urn:oasis:names:tc:SAML:2.0:nameid-format:transient">
              3f7b3dcf-1674-4ecd-92c8-1544f346baf8
            </saml:NameID>
            <saml:SubjectConfirmation
              Method="urn:oasis:names:tc:SAML:2.0:cm:bearer">
              <saml:SubjectConfirmationData
                InResponseTo="identifier_1"
                Recipient="https://sp.example.com/SAML2/SSO/POST"
                NotOnOrAfter="2004-12-05T09:27:05Z"/>
            </saml:SubjectConfirmation>
          </saml:Subject>
          <saml:Conditions
            NotBefore="2004-12-05T09:17:05Z"
            NotOnOrAfter="2004-12-05T09:27:05Z">
            <saml:AudienceRestriction>
              <saml:Audience>https://sp.example.com/SAML2</saml:Audience>
            </saml:AudienceRestriction>
          </saml:Conditions>
          <saml:AuthnStatement
            AuthnInstant="2004-12-05T09:22:00Z"
            SessionIndex="identifier_3">
            <saml:AuthnContext>
              <saml:AuthnContextClassRef>
                urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport
              </saml:AuthnContextClassRef>
            </saml:AuthnContext>
          </saml:AuthnStatement>
        </saml:Assertion>
    </samlp:Response>"""

    def __init__(self, username, first_name, last_name, email,
                 destination):
        self.root = ET.fromstring(self.SAMPLE_RESPONSE)

    def to_string(self):
        return ET.tostring(self.root, encoding='utf8', method='xml')
