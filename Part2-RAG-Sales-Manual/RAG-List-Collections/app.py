from pymilvus import connections, utility
from flask import Flask, request, make_response
from flask_cors import CORS, cross_origin
import os
import logging

app = Flask(__name__)
CORS(app) 


app = Flask(__name__)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

@app.route('/', methods=["GET", "OPTIONS"])
def index():
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_preflight_response()
    elif request.method == "GET": # The actual request following the preflight
        content = {}
        
        MILVUS_HOST="milvus-service"
        MILVUS_PORT="19530"
        
        connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)
        app.logger.info('Connected to Milvus Host '+MILVUS_HOST)
        
        Collections = utility.list_collections()
        app.logger.info('Found collections:', Collections)
        
        content['result'] = Collections   
        return _corsify_actual_response(content)
    else:
        raise RuntimeError("Weird - don't know how to handle method {}".format(request.method))

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "https://rag-webpage-llm-on-techzone.apps.p1296.cecc.ihost.com")
    response.headers.add('Access-Control-Allow-Headers', "https://rag-webpage-llm-on-techzone.apps.p1296.cecc.ihost.com")
    response.headers.add('Access-Control-Allow-Methods', "https://rag-webpage-llm-on-techzone.apps.p1296.cecc.ihost.com")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "https://rag-webpage-llm-on-techzone.apps.p1296.cecc.ihost.com")
    return response

@app.route('/healthz')
# Added healthcheck endpoint
def healthz():
    return "ok"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
