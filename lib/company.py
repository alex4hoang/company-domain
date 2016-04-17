#!/usr/bin/python

class Company:

	def __init__(self, data):
		if not data:
			return False
		self.data = data

	def clean(self):
		output = []

		for row in self.data:
			items = {}
			for key in row:
				items[key[4:].strip('_')] = row[key]
			output.append(items)
		return output

	def simple_cleaner(self):
		output = ''
		output = self.data.lower()

		dont_want = ['inc', 'incorporated', 'llc', 'llp', 'plc', 'ltd', 'limited', 'gmbh',
					'corporation']

		for common_suffix in dont_want:
			if common_suffix in output:
				output = output.replace(common_suffix, '')

		output = output.strip(' .,')
		return output
