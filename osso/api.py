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
import urllib

from osso import config
from osso import saml
from osso import server

SAML_REQUEST_PARAM = 'SAMLRequest'
RELAY_STATE_PARAM = 'RelayState'


@server.app.route('/saml/redirect')
def post():
    saml_request = server.request.args.get(SAML_REQUEST_PARAM, None)
    saml_request = urllib.unquote(saml_request).decode('utf8')
    relay_state = server.request.args.get(RELAY_STATE_PARAM, None)
    if not saml_request:
        server.abort(400)

    request = saml.AuthenticationRequest(saml_request)
    endpoint = config.SERVICE_PROVIDERS[request.issuer]['POST']
    # TODO(knikolla): Get values from environment
    # TODO(knikolla): Build SAML response
    response = saml.AuthenticationResponse('username',
                                           'first_name',
                                           'last_name',
                                           'email',
                                           request.issuer)
    response = base64.b64encode(response.to_string())

    return server.render_template('saml_form.html',
                                  saml_endpoint=endpoint,
                                  saml_response=response,
                                  relay_state=relay_state)


if __name__ == '__main__':
    server.app.run(host='0.0.0.0', threaded=True)
