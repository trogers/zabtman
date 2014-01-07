#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# zabtman - Zabbix Template Manager
# Copyright © 2013 Greg Swift gregswift@gmail.com
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

__version__ = '0.0.1'
__license__ = 'GPLv3+'
__author__ = 'Greg Swift'
__author_email__ = 'gregswift@gmail.com'

import requests
try:
    import json
except ImportError:
    import simplejson as json

TIMEOUT = 30
HEADERS = {'Content-Type': 'application/json',
        'User-Agent': 'python/zabbix_api'}
IMPORT_RULES = {
    'templates': {
        'createMissing': True,
        'updateExisting': True
    },
    'templateLinkage': {
        'createMissing': True
    },
    'hosts': {
        'createMissing': True,
        'updateExisting': True
    },
    'items': {
        'createMissing': True,
        'updateExisting': True
    },
    'graphs': {
        'createMissing': True,
        'updateExisting': True
    },
    'triggers': {
        'createMissing': True,
        'updateExisting': True
    },
    'applications': {
        'createMissing': True,
        'updateExisting': True
    }
}


class ZabbixTemplateAPIException(Exception):
    pass

class ZabbixTemplateAPI(object):
    auth_key = None
    id = 0

    def __init__(self, url, user, passwd, timeout=None, headers=None):
        self.url = url
        self.user = user
        self.passwd = passwd
        self.timeout = timeout
        if timeout is None:
            self.timeout = TIMEOUT
        self.headers = headers
        if headers is None:
            self.headers = HEADERS
        self.auth()

    def __call_api(self, method, params={}):
        obj = { 'jsonrpc': '2.0',
                'method': method,
                'params': params,
                'auth': self.auth_key,
                'id': self.id
        }
        result = requests.get(self.url,
                headers=self.headers,
                data=json.dumps(obj),
                verify=False,
                allow_redirects=True)
        result.raise_for_status()
        self.id += 1
        return result.json()


    def auth(self):
        if self.auth_key is None:
            method = 'user.authenticate'
            params = { 'user': self.user,
                   'password': self.passwd
            }
            results = self.__call_api(method, params)
            self.auth_key = results['result']
        return self.auth_key

    def export_json(self, templates):
        method = 'configuration.export'
        params = { 'format': 'json',
                'options': {
                        'templates': templates
                }
        }
        result = self.__call_api(method, params)['result']
        return json.dumps(result,indent=2)

    def import_json(self, source, rules=None):
        if rules is None:
            rules = IMPORT_RULES
        method = 'configuration.import'
        params = { 'format': 'json',
                'source': source,
                'rules': rules,
        }
        ret = self.__call_api(method, params)
        try:
          return ret['error']
        except KeyError:
          return ret['result']
