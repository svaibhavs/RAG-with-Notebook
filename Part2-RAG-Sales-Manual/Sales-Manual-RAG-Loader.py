#!/usr/bin/env python
# coding: utf-8

from pymilvus import connections, utility
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Milvus
from langchain.document_loaders import WebBaseLoader, PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
import os

MILVUS_HOST="milvus-service"
MILVUS_PORT="19530"

LLAMA_HOST="llama-service"
LLAMA_PORT="8080"

connections.connect(host="milvus-service", port="19530")

Server_Name = "IBM Power S1014"

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
