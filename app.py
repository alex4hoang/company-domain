#!/usr/bin/python

# Additional Readings:
# http://stackoverflow.com/questions/11228153/bottle-framework-with-multiple-files
# https://taoofmac.com/space/blog/2013/08/11/2300#
# https://www.toptal.com/bottle/building-a-rest-api-with-bottle-framework
# http://www.tengiz.net/bootlepy-nginx-uwsgi-python3-with-virtualenv-on-debian/
# http://uwsgi-docs.readthedocs.org/en/latest/WSGIquickstart.html

import os, bson, json, bottle, bottle_pgsql, pprint, time

from bottle import hook, route, template, run, debug, get, post, request, static_file, response
from lib.company import *
from lib.freebase import *

app = application = bottle.Bottle()

# debug(True)

##
# Config file
with open('/pie.cfg') as pie_cfg:
	cfg = json.load(pie_cfg)

##
# Connect to db
db_plugin = bottle_pgsql.Plugin('dbname=' + cfg['local_postgres']['db'] +
								' user=' + cfg['local_postgres']['user'] +
								' password=' + cfg['local_postgres']['passwd'] +
								' port=' + cfg['local_postgres']['port'])
app.install(db_plugin)


##
# Get that slash out of the request
@app.hook('before_request')
def strip_path():
	RateLimited(5)
	request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')

##
# Limit api call
def RateLimited(maxPerSecond = None):
	if not maxPerSecond:
		maxPerSecond = 5

	minInterval = 1.0 / float(maxPerSecond)
	lastTimeCalled = [0.0]
	elapsed = time.clock() - lastTimeCalled[0]
	leftToWait = minInterval - elapsed

	if leftToWait>0:
		time.sleep(leftToWait)

	lastTimeCalled[0] = time.clock()

##
# The front "index" page
@app.route('/')
def show_index():
	return static_file('index.html', root='./static')

##
# Serve template
@app.route('/company', method='GET')
def show_tpl():
	return template('search', text="Enter a Company Name... (ie. Google, Inc.)")

##
# Serve template
@app.route('/domain', method='GET')
def show_tpl():
	return template('search', text="Enter a Domain... (ie. google.com)")

##
# Serve static files
@app.route('/static/<filename:path>')
def static(filename):
	return static_file(filename, root='./static')

##
# Get domain match from company_name
@app.route('/company/<company_name>', method='GET')
def show_json(company_name, db):
	data = {}
	cc = Company(company_name)
	company_name_input = cc.simple_cleaner()

	sql = """SELECT cdr_source, cdr_company_name, cdr_domain
			FROM company_domain_rel
			WHERE cdr_company_name ILIKE %s
			ORDER BY cdr_d_id, LENGTH(cdr_company_name) ASC
			LIMIT 2;"""

	try:
		db.execute( sql, (company_name_input + '%',) )
		data = db.fetchall()
	except:
		output = { 'status': 'internal server error', 'message': 'Unable to connect to DB.' }
		response.status = 500
		return '{}'.format(json.dumps(output, indent=4, default=json_util.default))

	response.content_type='application/vnd.api+json'

	if data:
		cc = Company(data)
		jsondata = cc.clean()
		if jsondata:
			output = { 'status': 'success', 'data': jsondata }
			response.status = 200
			return '{}'.format(json.dumps(output, indent=4, default=json_util.default))

	output = { 'status': 'not found', 'message': 'Please try another identifier.' }
	response.status = 404
	return '{}'.format(json.dumps(output, indent=4, default=json_util.default))

##
# Get company match from domain
@app.route('/domain/<domain>', method='GET')
def show_json(domain, db):
	data = {}
	if 'www.' in domain:
		domain = domain.replace('www.', '')
	if '.' not in domain:
		domain = domain + '.com'

	sql = """SELECT cdr_source, cdr_company_name, cdr_domain
			FROM company_domain_rel
			WHERE cdr_domain ILIKE %s
			ORDER BY cdr_d_id, LENGTH(cdr_company_name) ASC
			LIMIT 2;"""

	try:
		db.execute( sql, (domain + '%',) )
		data = db.fetchall()
	except:
		output = { 'status': 'internal server error', 'message': 'Unable to connect to DB.' }
		response.status = 500
		return '{}'.format(json.dumps(output, indent=4, default=json_util.default))

	response.content_type='application/vnd.api+json'

	if data:
		cc = Company(data)
		jsondata = cc.clean()
		if jsondata:
			output = { 'status': 'success', 'data': jsondata }
			response.status = 200
			return '{}'.format(json.dumps(output, indent=4, default=json_util.default))

	output = { 'status': 'not found', 'message': 'Please try another identifier.' }
	response.status = 404
	return '{}'.format(json.dumps(output, indent=4, default=json_util.default))


##
# Run app
if __name__ == '__main__':
	run(app=app,
		host='0.0.0.0',
		port=8081)
