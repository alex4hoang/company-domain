#!/usr/bin/python

import os, psycopg2, psycopg2.extras, json

class DB:

	def connect(self):
		""" Connect to Postgres DB
		@return [conn] cursor
		"""

		# Config file
		with open('/pie.cfg') as pie_cfg:
			cfg = json.load(pie_cfg)

		# Connect to db
		try:
		    conn = psycopg2.connect('dbname=' + cfg['local_postgres']['db'] +
								' user=' + cfg['local_postgres']['user'] +
								' password=' + cfg['local_postgres']['passwd'] +
								' port=' + cfg['local_postgres']['port'])
		    conn.autocommit = True
		except:
		    print "Cannot connect to db"
		    return False

		return conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
