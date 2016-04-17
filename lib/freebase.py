#!/usr/bin/python

import os, json, pprint

from bson import json_util
from DB import DB
from phpserialize import serialize, unserialize
from urlparse import urlparse

# Related links:
# http://www.utf8-chartable.de/unicode-utf8-table.pl?start=128&number=128&names=-&utf8=string-literal
# SELECT d_id, d_domain, fbc_id, fbc_company_name, fbc_full_url FROM domains JOIN freebase_companies ON d_domain = fbc_domain ORDER BY d_id LIMIT 1000;
# SELECT fbc_domain, COUNT(fbc_domain) FROM freebase_companies GROUP BY fbc_domain ORDER BY COUNT(fbc_domain) DESC;
#
# UPDATE freebase_companies SET fbc_domain = '' WHERE fbc_id IN ('m.03gg6vm','m.06gb9p');
# SELECT * FROM freebase_companies WHERE fbc_id IN ('m.03gg6vm','m.06gb9p');
#
# SELECT fbc_domain, COUNT(fbc_domain) FROM freebase_companies GROUP BY fbc_domain ORDER BY COUNT(fbc_domain) DESC;
#
# Main selects:
# SELECT cn_id, d_id, 1, fbc_company_name, fbc_domain FROM domains
# JOIN freebase_companies ON d_domain = fbc_domain
# JOIN company_names ON fbc_company_name = cn_company_name
# ORDER BY d_id LIMIT 100;



class Freebase:

	def __init__(self, fbc_id):
		self.fbc_id = fbc_id
		self.DB = DB().connect()

	def get_single_data(self, fbc_id):
		""" Get data from a single fbc_id
		@return [tuple]
		"""
		if not fbc_id:
			return False

		sql = 'SELECT * FROM freebase_companies WHERE fbc_id = %s LIMIT 1;'
		self.DB.execute(sql, (fbc_id,))
		data = self.DB.fetchone()

		return data

	def get_next_data(self, last_fbc_id):
		""" Get data from the fbc_id after current
		@return [tuple]
		"""
		if not last_fbc_id:
			return False

		sql = 'SELECT * FROM freebase_companies WHERE fbc_id > %s ORDER BY fbc_id ASC LIMIT 1;'
		self.DB.execute(sql, (last_fbc_id,))
		data = self.DB.fetchone()

		return data

	def parse_out_domain(self, full_url):
		""" Parse out http:// and return clean domain
		@return [str]
		"""
		if not full_url:
			return False

		try:
			parsed_url = urlparse(full_url)
		except:
			return False
		if parsed_url.netloc:
			if 'www.' in parsed_url.netloc[:4]:
				return parsed_url.netloc[4:]
			else:
				return parsed_url.netloc
		return False

	def run_parse_all_domains(self, last_fbc_id):
		""" Loop through all fbc_ids and parse out domain with script:
				Fb = Freebase('');
				last_id = 'm'
				for x in range(1,300000):
					last_id = Fb.run_parse_all_domains(last_id)

		@return [str] last_fbc_id
		"""
		if not last_fbc_id:
			return False

		update_sql = "UPDATE freebase_companies SET fbc_domain = %s WHERE fbc_id = %s;";

		data = Fb.get_next_data(last_fbc_id);
		if data:
			domain = Fb.parse_out_domain(data['fbc_full_url'])
			if domain:
				try:
					# self.DB.execute(update_sql, (domain, data['fbc_id']))
					print self.DB.mogrify(update_sql, (domain, data['fbc_id']))
					print self.DB.statusmessage
				except:
					print 'Failed insert, already exists: ' + data['fbc_id']
			return data['fbc_id']
		return False

	def run_clean_all_domains(self, last_fbc_id):
		""" Loop through all fbc_ids and set domain = '' with script:
				Fb = Freebase('');
				last_id = '0'
				for x in range(1,300000):
					last_id = Fb.run_clean_all_domains(last_id)

		@return [str] last_fbc_id
		"""
		if not last_fbc_id:
			return False

		update_sql = "UPDATE freebase_companies SET fbc_domain = '' WHERE fbc_id = %s;"

		data = Fb.get_next_data(last_fbc_id);

		if data and data['fbc_full_url']:
			try:
				parsed_url = urlparse(data['fbc_full_url'])
			except:
				return data['fbc_id']
			if len(parsed_url.path.strip()) > 1:
				try:
					# self.DB.execute(update_sql, (data['fbc_id'],))
					print self.DB.mogrify(update_sql, (data['fbc_id'],))
					print self.DB.statusmessage
				except:
					print self.DB.mogrify(update_sql, (data['fbc_id'],))
					print 'Failed update, for: ' + data['fbc_id']

			return data['fbc_id']
		return False

