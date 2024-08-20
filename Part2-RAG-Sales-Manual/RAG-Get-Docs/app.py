from pymilvus import connections, utility
from flask import Flask, request
import os
import logging

app = Flask(__name__)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

@app.route('/')
def index():
    content = {}

    if request.args.get('Server_Name'):
        Server_Name = request.args.get('Server_Name')
        app.logger.info('Found Server_Name '+Server_Name)
        
        MILVUS_HOST="milvus-service"
        MILVUS_PORT="19530"

        connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)
        app.logger.info('Connected to Milvus Host '+MILVUS_HOST)

        vector_store = Milvus(
            collection_name="sales_manuals",
            connection_args={"host": MILVUS_HOST, "port": MILVUS_PORT}
        )

        FNAME = Server_Name+".pdf"

        questions = ["How many dual-chip processor modules in the server?", "How Power10 processors in the server?", "What speed in GHz are the processors in the server?"]
        question = questions[0]

        docs = vector_store.similarity_search_with_score(question, k=3, expr="source == FNAME")
        app.logger.info('Got docs from vector store')
        
        content['result'] = "Success", docs
    else:
        content ['result'] = "Server Name Missing"
        
    return content

@app.route('/healthz')
# Added healthcheck endpoint
def healthz():
    return "ok"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
