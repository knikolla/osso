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
import jwt

from osso import config
from osso import pki


def get_config(url_root):
    return json.dumps(
        {
            'issuer': config.IDP_ENTITY_ID,
            'authorization_endpoint': '%s/connect/authorize' % url_root,
            'token_endpoint': '%s/connect/token' % url_root,
            'jwks_uri': '%s/connect/certs'
        }
    )


def get_certs():
    return json.dumps(
        {
            'kid': '',
            'kty': 'RSA',
            'alg': 'RS256',
            'use': 'sig',
            'n': pki.PUBLIC.key_oneline
        }
    )


class AuthorizationRequest(object):
    CLIENT_ID_QUERY_PARAM = 'client_id'
    CLIENT_SECRET_QUERY_PARAM = 'client_secret'
    REDIRECT_URI_QUERY_PARAM = 'redirect_uri'
    SCOPE_QUERY_PARAM = 'scope'
    RESPONSE_TYPE_QUERY_PARAM = 'response_type'
    STATE_QUERY_PARAM = 'state'

    @classmethod
    def from_request(cls, request):
        return AuthorizationRequest(
            request.args.get(cls.CLIENT_ID_QUERY_PARAM),
            request.args.get(cls.CLIENT_SECRET_QUERY_PARAM),
            request.args.get(cls.REDIRECT_URI_QUERY_PARAM),
            request.args.get(cls.SCOPE_QUERY_PARAM),
            request.args.get(cls.RESPONSE_TYPE_QUERY_PARAM),
            request.args.get(cls.STATE_QUERY_PARAM)
        )

    def __init__(self, client_id, client_secret, redirect_uri, scope,
                 response_type, state):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri,
        self.scope = scope
        self.response_type = response_type
        self.state = state

        self.authorize_client(self.client_id,
                              self.client_secret,
                              self.redirect_uri)

    @classmethod
    def authorize_client(cls, client_id, client_secret, redirect_uri):
        # TODO: Compare client_id and secret from config file
        # TODO: Compare redirect_uri from config file for authed client
        pass


class AuthenticationResponse(object):
    def __init__(self, username):
        self.username = username

    @property
    def authorization_code(self):
        payload = {
            'iss': config.IDP_ENTITY_ID,
        }

    @property
    def access_token(self):
        payload = {
            'iss': config.IDP_ENTITY_ID,
            'sub': self.username,
        }
        return jwt.encode(payload, config.JWT_ACCESS_TOKEN_SECRET)

