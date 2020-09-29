#!/usr/bin/env python

import sys
import json
from datetime import datetime

import psycopg2
try:
    conn = psycopg2.connect("dbname='db' user='writer' host='db' password='writer'")
except:
    print 'I am unable to connect to the database'
    sys.exit(1)


from flask import Flask, request
app = Flask(__name__)

@app.route('/log', methods=['POST'])
def log():
    data = json.loads(request.data)
    if request.headers.getlist("X-Forwarded-For"):
      ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
      ip = request.remote_addr
    cur = conn.cursor()
    cur.execute('INSERT INTO events (timestamp, type, payload, ip_address) VALUES (%s, %s, %s, %s)', (
      datetime.now(),
      data["type"],
      data["payload"],
      ip
    ))
    conn.commit()
    return "OK"

if __name__ == '__main__':
    app.run()
