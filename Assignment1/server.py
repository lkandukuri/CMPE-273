#!/usr/bin/env python
from flask import Flask, request, jsonify, json
import rocksdb
import uuid
import sys
import StringIO
import contextlib

app = Flask(__name__)
	
@app.route('/api/v1/scripts', methods = ['POST'])
def upload_file():
	f = request.files['data']
	db = rocksdb.DB("test.db", rocksdb.Options(create_if_missing=True))
	key = uuid.uuid4().hex
	db.put(key.encode('utf-8'),f.stream.read().encode('utf-8'))

	return jsonify(scriptid = key),201


# To execute python script foo.py, playing with console output
@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


@app.route('/api/v1/scripts/<scriptid>', methods = ['GET'])
def retrieve_file(scriptid=None):

	db = rocksdb.DB("test.db", rocksdb.Options(create_if_missing=True))
	value = db.get(scriptid.encode('utf-8'))

	with stdoutIO() as s:
		exec value

	return s.getvalue()



if __name__ == '__main__':
   app.run(debug = True, port=8000)