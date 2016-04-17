#!/usr/bin/python

import os, sys, json, pprint
sys.path.append("/var/www/html/")

from bson import json_util
from lib.DB import DB
from phpserialize import serialize, unserialize
from urlparse import urlparse

domain = 'facebook.com'


DB = DB().connect()

sql = "SELECT fbc_company_name FROM freebase_companies;"
try:
	DB.execute(sql, ())
	data = DB.fetchall()
except:
	print 'Sorry, something went wrong!'


insert_sql = "INSERT INTO company_names (cn_company_name) VALUES(%s);"

if data:
	for d in data:
		if d['fbc_company_name']:
			try:
				# DB.execute(insert_sql, (d['fbc_company_name'],))
				print DB.mogrify(insert_sql, (d['fbc_company_name'],))
				print DB.statusmessage
			except:
				print 'Failed insert, already exists: ' + d['fbc_company_name']

