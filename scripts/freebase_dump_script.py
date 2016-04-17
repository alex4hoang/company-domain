#!/usr/bin/python

# SELECT * FROM freebase_companies WHERE fbc_domain LIKE '%qq.com%' LIMIT 20;
# http://localhost:7777/freebase/get/m.02hqcn #not processed
#
# SELECT * FROM freebase_companies WHERE fbc_domain LIKE '%sina.com%' ORDER BY LENGTH(fbc_domain) ASC LIMIT 20;

import os, sys
sys.path.append("/var/www/html/")
from lib.freebase_dump import FreebaseDump

FB = FreebaseDump('')

# Last: m.0sl2w
last_id = 'n.'
count = 0

for x in range(0,1000000):
	last_id = FB.run_save_script(last_id, FB.UPPER_LIMIT_N_0)
	count += 1

print 'Finished! count: ' + str(count)
