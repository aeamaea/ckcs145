import logging

from flask import Flask, request, jsonify, render_template
from dotenv import dotenv_values
from datetime import datetime

# get secrets from the .env file 
config=dotenv_values(".env")

import pugsql 
queries = pugsql.module('queries/')
queries.connect('postgresql://'+config["PG_USER"]+':'+config["PG_PASS"]+'@localhost:5432/jwfoods')


"""
 Logging configuration
"""

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def homepage():
	visit_ip = request.remote_addr
	visit_time = datetime.now()
	insert_retcode = queries.insert_visit(visit_time=visit_time, visit_ip=visit_ip)
	print("insert return code: ", insert_retcode)

	return render_template('company.html')

if __name__=="__main__":
	app.run(host='0.0.0.0', port=5000, debug=True)
