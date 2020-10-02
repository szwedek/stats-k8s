#!/usr/bin/env python

import sys
import os
import json
import logging
from datetime import datetime

import psycopg2
try:
    conn = psycopg2.connect("dbname=%s user=%s host=%s password=%s" % (os.environ['DB_NAME'], os.environ['DB_USER'], os.environ['DB_HOST'], os.environ['DB_PASS']))
except:
    print('I am unable to connect to the database')
    sys.exit(1)


from flask import Flask, request
from gevent.pywsgi import WSGIServer
app = Flask(__name__)
app_health = Flask(__name__)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

@app.route('/log', methods=['POST'])
def log():
    data = request.json
    cur = conn.cursor()
    cur.execute('INSERT INTO events (timestamp, type, payload) VALUES (%s, %s, %s)', (
      datetime.now(),
      data["type"],
      data["payload"]
    ))
    conn.commit()
    return "OK"

@app_health.route('/healthz')
def heatlth():
    return "OK"

https_server = WSGIServer(('0.0.0.0', 80), app, log=logger)
https_server.start()

http_server = WSGIServer(('0.0.0.0', 81), app_health, log=logger)
http_server.serve_forever()
