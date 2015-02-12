# -*- coding: UTF-8 -*-

__author__ = 'luyu'

import requests

r = requests.get('http://pd.autotiming.com/users/current.json', auth=('luyu', 'dope54rna'))
if r.status_code == 200:
    user = r.json()
else:
    user = None

# {u'user': {u'last_login_on': u'2014-01-20T06:53:36Z', u'firstname': u'Luyu', u'lastname': u'Zhang', u'created_on': u'2013-07-31T15:41:15Z', u'mail': u'luyu.zhang@autotiming.com', u'login': u'luyu', u'api_key': u'3c1ad35e878db15ef0d36d626c4265b6e0b329b7', u'id': 22}}
print user