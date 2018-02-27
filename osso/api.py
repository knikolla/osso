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

from osso import auth
from osso import config
from osso import saml
from osso import server

SAML_REQUEST_PARAM = 'SAMLRequest'
RELAY_STATE_PARAM = 'RelayState'


@server.app.route('/saml/redirect')
def post():
    saml_request = server.request.args.get(SAML_REQUEST_PARAM, None)
    if not saml_request:
        server.abort(400)
    saml_request = saml.decode_saml_request(saml_request)

    relay_state = server.request.args.get(RELAY_STATE_PARAM, None)
    # TODO(knikolla): Validate relay_state < 80 bytes

    request = saml.AuthenticationRequest(saml_request)
    endpoint = config.SAML_SP[request.issuer]['bindings']['POST']

    user = auth.auth()
    response = saml.AuthenticationResponse(user.username,
                                           user.first_name,
                                           user.last_name,
                                           user.email,
                                           request.issuer,
                                           request.id)

    return server.render_template('saml_form.html',
                                  saml_endpoint=endpoint,
                                  saml_response=response.encoded(),
                                  relay_state=relay_state)


@server.app.route('/saml/metadata')
def metadata():
    return server.Response(saml.get_metadata(server.request.url_root),
                           mimetype='application/xml')


@server.app.route('/saml/info')
def info():
    user = auth.auth()
    return server.render_template('saml_info.html',
                                  username=user.username,
                                  first_name=user.first_name,
                                  last_name=user.last_name,
                                  email=user.email,
                                  info=str(server.request.environ))


if __name__ == '__main__':
    server.app.run(host='0.0.0.0', threaded=True)
