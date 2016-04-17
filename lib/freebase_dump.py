#!/usr/bin/python

import os, json, pprint

from bson import json_util
from DB import DB
from phpserialize import serialize, unserialize

# Related links:
# http://www.utf8-chartable.de/unicode-utf8-table.pl?start=128&number=128&names=-&utf8=string-literal
# Freebase Dump: https://developers.google.com/freebase/data

class FreebaseDump:
	""" Functions to mine the Freebase dump
	"""

	NUMBER_ROWS_TO_FETCH = 100
	UPPER_LIMIT_M_0 = 'm.1'
	UPPER_LIMIT_N_0 = 'n.1'
	UPPER_LIMIT_G_0 = 'g.1'

	def __init__(self, fb_id):
		self.fb_id = fb_id
		self.DB = DB().connect()

	def run_save_script(self, id_last, upper_limit):
		""" Run batch save script
		@return [str] last_id
		"""
		fb_ids = self.get_batch_ids(id_last, upper_limit)
		if not fb_ids:
			return False

		for fb_id in fb_ids:
			single_data = self.get_single_data(fb_id)
			good_data = self.parse_out_wanted_data(single_data)
			if good_data:
				self.save_new_data(good_data)

		if fb_ids:
			# last id of batch
			return fb_ids[-1:][0]
		else:
			return None

	def get_single_data(self, fb_id):
		""" Get data from a single fb_id
		@return [tuple]
		"""
		if not fb_id:
			return False

		sql = 'SELECT * FROM freebase_dump WHERE fb_id = %s LIMIT 1;'
		self.DB.execute(sql, (fb_id,))
		data = self.DB.fetchone()

		return data

	def get_batch_ids(self, id_last, upper_limit):
		""" Get a batch of ids
		@return [list]
		"""
		if not id_last:
			return False
		if not upper_limit:
			upper_limit = 'z'

		sql = 'SELECT fb_id FROM freebase_dump WHERE fb_id > %s AND fb_id < %s ORDER BY fb_id ASC LIMIT ' + \
			str( self.NUMBER_ROWS_TO_FETCH ) + ';'

		self.DB.execute(sql, (id_last, upper_limit,))

		data = self.DB.fetchall()
		fb_ids = [d[0] for d in data]

		if fb_ids:
			return fb_ids
		else:
			return None

	def parse_out_wanted_data(self, data):
		""" Parse out wanted data: company_name and domain
		company_name = "rdf-schema#label.en", "rdf-schema#label"
		website = "common.topic.official_website"
		@return [dict]
		"""
		if not data:
			return False
		if type(data) is not tuple:
			return False

		fb_id = data[0]
		wants = ('business', 'company', 'companies', 'corporation', 'corporated')

		if any(needle in data[1].lower() for needle in wants):
			try:
				udata = unserialize(data[1])
			except:
				return False

			good_data = {}

			if 'rdf-schema#label.en' in udata:
				good_data['company_name'] = udata['rdf-schema#label.en']
			elif 'rdf-schema#label' in udata:
				good_data[ 'company_name' ] = udata[ 'rdf-schema#label' ]

			if 'common.topic.official_website' in udata:
				good_data[ 'website' ] = udata[ 'common.topic.official_website' ][0]

			if 'website' in good_data:
				good_data['fb_id'] = fb_id
				return good_data
		else:
			return False

	def save_new_data(self, data_dict):
		""" Saves new data
		@return [bool]
		"""
		if not data_dict:
			return False
		if type(data_dict) is not dict:
			return False

		insert_sql = "INSERT INTO freebase_companies (fbc_id, fbc_company_name, fbc_domain) VALUES(%s, %s, %s);";

		if all(keys in data_dict for keys in ('fb_id', 'company_name', 'website')):
			try:
				self.DB.execute(insert_sql, (data_dict['fb_id'], data_dict['company_name'], data_dict['website']))
				print self.DB.mogrify(insert_sql, (data_dict['fb_id'], data_dict['company_name'], data_dict['website']))
				print self.DB.statusmessage
				return True
			except:
				print 'Failed insert, already exists: ' + data_dict['fb_id']
		else:
			print 'Failed insert, not enough data.'
			print data_dict

		return False
