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
from zabtman import ZabbixTemplateAPI
from os.path import expanduser
import argparse
import ConfigParser
import sys
import json
def run():
  parser = argparse.ArgumentParser(prog='zabtman',description='Zabbix Template Manager')
  parser.add_argument('--environment', help='section from config file', required=True)
  parser.add_argument('--filename', help='filename of import/export', required=True)
  parser.add_argument('action', help='import|export')
  parser.add_argument('--templates', help='template ids (comma-separated)')

  args = parser.parse_args()
  Config = ConfigParser.ConfigParser()
  # get user's home directory
  homedir = expanduser("~")
  Config.read(homedir+'/.zabbix')
  url = Config.get(args.environment,'url')
  user = Config.get(args.environment,'user')
  password = Config.get(args.environment,'pass')
  zabt = ZabbixTemplateAPI(url, user, password)
  if args.action == 'import':
    f = open(args.filename, 'r')
    print 'Importing '+args.filename
    data = f.read()
    ret = zabt.import_json(data)
    try:
      print ret['data']
    except TypeError:
      print 'Import Successful'
  elif args.action == 'export':
    if args.templates is not None:
      f = open(args.filename, 'w')
      print 'Exporting to '+args.filename
      ret = zabt.export_json(args.templates)
      f.write(json.loads(ret))
    else:
      print 'Error: Must include --template when exporting.'
      sys.exit(1)
  else:
    print 'Action must be import or export.'
