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

AUTH_REQUEST = """
<samlp:AuthnRequest
     xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
     xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"
     ID="identifier_1"
     Version="2.0"
     IssueInstant="2004-12-05T09:21:59Z"
     AssertionConsumerServiceIndex="1">
     <saml:Issuer>https://sp.example.com/SAML2</saml:Issuer>
     <samlp:NameIDPolicy
       AllowCreate="true"
       Format="urn:oasis:names:tc:SAML:2.0:nameid-format:transient"/>
</samlp:AuthnRequest>
"""
