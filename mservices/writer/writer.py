#!/usr/bin/env python

import sys
import os
import json
from datetime import datetime

import psycopg2
try:
    conn = psycopg2.connect("dbname=%s user=%s host=%s password=%s" % (os.environ['DB_NAME'], os.environ['DB_USER'], os.environ['DB_HOST'], os.environ['DB_PASS']))
except:
    print('I am unable to connect to the database')
    sys.exit(1)


from flask import Flask, request
app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
