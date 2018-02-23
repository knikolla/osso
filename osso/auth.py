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

import os


def auth():
    return User()


class User(object):
    def __init__(self):
        self.username = os.environ['eppn']
        self.first_name = os.environ['givenName']
        self.last_name = os.environ['sn']
        self.email = os.environ['mail']
