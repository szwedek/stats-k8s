#!/usr/bin/env python

import sys
import json
import os
import logging
import psycopg2
try:
    conn = psycopg2.connect("dbname=%s user=%s host=%s password=%s" % (os.environ['DB_NAME'], os.environ['DB_USER'], os.environ['DB_HOST'], os.environ['DB_PASS']))
except:
    print('I am unable to connect to the database')
    sys.exit(1)


from flask import Flask
from gevent.pywsgi import WSGIServer
app = Flask(__name__)
app_health = Flask(__name__)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

@app.route('/stats')
def stats():
    cur = conn.cursor()
    cur.execute('SELECT type, count(*) FROM events GROUP BY type')
    rows = cur.fetchall()
    cur.close()
    return json.dumps(dict(map(lambda x: (x[0], int(x[1])), rows)))

@app_health.route('/healthz')
def heatlth():
    return "OK"

http_server = WSGIServer(('0.0.0.0', 81), app_health, log=logger)
http_server.start()

https_server = WSGIServer(('0.0.0.0', 80), app, log=logger)
https_server.serve_forever()
