from pymilvus import connections, utility
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Milvus
from langchain.document_loaders import WebBaseLoader, PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    content = {}

    if request.args.get('Server_Name'):
        Server_Name = request.args.get('Server_Name')
        content['result'] = "Found Server_Name"
        content['Server_Name'] = Server_Name
        
        MILVUS_HOST="milvus-service"
        MILVUS_PORT="19530"

        LLAMA_HOST="llama-service"
        LLAMA_PORT="8080"

        connections.connect(host="milvus-service", port="19530")
        
        FNAME = Server_Name+".pdf"
        
        loader = PyPDFLoader(FNAME)
        
        docs = loader.load()
        
        text_splitter = CharacterTextSplitter(separator="\n", chunk_size=768, chunk_overlap=0)
        docs = text_splitter.split_documents(docs)
        len(docs)
        
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        vector_store = Milvus.from_documents(
            docs,
            embedding=embeddings,
            collection_name="sales_manuals",
            connection_args={"host": MILVUS_HOST, "port": MILVUS_PORT}
        )
        
        utility.list_collections()
        
        content['result'] = "Success"
    else:
        content ['result'] = "MTM Missing"
        
    return content

@app.route('/healthz')
# Added healthcheck endpoint
def healthz():
    return "ok"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
