#!/usr/bin/python

import os, sys, json, pprint
sys.path.append("/var/www/html/")

from bson import json_util
from lib.DB import DB
from phpserialize import serialize, unserialize
from urlparse import urlparse

DB = DB().connect()

sql = """
	SELECT cn_id, d_id, 1 as num, fbc_company_name, fbc_domain FROM domains
	JOIN freebase_companies ON d_domain = fbc_domain
	JOIN company_names ON fbc_company_name = cn_company_name;
	"""
try:
	DB.execute(sql, ())
	data = DB.fetchall()
except:
	print 'Sorry, something went wrong!'


insert_sql = "INSERT INTO company_domain_rel (cdr_cn_id, cdr_d_id, cdr_source, cdr_company_name, cdr_domain) VALUES(%s, %s, %s, %s, %s);"

if data:
	for d in data:
		if d:
			try:
				DB.execute(insert_sql, (d['cn_id'],d['d_id'],d['num'],d['fbc_company_name'],d['fbc_domain'],))
				print DB.mogrify(insert_sql, (d['cn_id'],d['d_id'],d['num'],d['fbc_company_name'],d['fbc_domain'],))
				print DB.statusmessage
			except:
				print 'Failed insert, already exists: '
				print DB.mogrify(insert_sql, (d['cn_id'],d['d_id'],d['num'],d['fbc_company_name'],d['fbc_domain'],))

