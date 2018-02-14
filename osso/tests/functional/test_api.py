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

import pytest
from osso import api


class TestApi(object):
    @pytest.fixture()
    def app(self):
        return api.server.app.test_client()

    def test_redirect_no_saml_request(self, app):
        r = app.get('/saml/redirect')
        assert r.status_code == 400
