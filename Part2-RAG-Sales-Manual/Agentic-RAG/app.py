from pymilvus import connections, utility
from langchain_community.llms import LlamaCpp
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Milvus
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.prompts import PromptTemplate
from langchain.tools import tool
from langchain.tools.render import render_text_description_and_args
from langchain.agents.output_parsers import JSONAgentOutputParser
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents import AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnablePassthrough

from flask import Flask, request
from flask_cors import CORS, cross_origin
import os
import logging
import requests

app = Flask(__name__)
CORS(app, origins=["https://rag-webpage-llm-on-techzone.apps.cyan.pssc.mop.fr.ibm.com"]) 

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

@app.route('/')
@cross_origin() # allow all origins all methods.
def index():
    content = {}
    
    LLAMA_HOST="llama-service"
    LLAMA_PORT="8080"

#    llm = LlamaCpp(
#        temperature=0,
#        model_id= "ibm/granite-3-8b-instruct", 
#        params={
#            GenParams.DECODING_METHOD: "greedy",
#            GenParams.TEMPERATURE: 0,
#            GenParams.MIN_NEW_TOKENS: 5,
#            GenParams.MAX_NEW_TOKENS: 250,
#            GenParams.STOP_SEQUENCES: ["Human:", "Observation"],
#        },
#    )

    template = "Answer the {query} accurately. If you do not know the answer, simply say you do not know."
    prompt = PromptTemplate.from_template(template)

#    agent = prompt | llm

    json_data = {
        'prompt': prompt,
        'temperature': 0,
        'n_predict': 100,
        'stream': False,
    }
    
    app.logger.info('Sending request to the LLM with this JSON data: '+str(json_data))
        
    res = requests.post(f'http://{LLAMA_HOST}:{LLAMA_PORT}/completion', json=json_data, timeout=600)
    app.logger.info('Recieved this from the LLM: '+str(res.json()))
        
    answer = res.json()['content']
    content['result'] = "Success"
    content['answer'] = answer
  
    if request.args.get('Query'):
        Query = request.args.get('Query')

        app.logger.info('Found Query '+Query)
        
        agent.invoke({"query": Query})
        
        app.logger.info('Invoking Agent for '+Query)

        urls = [
            "https://www.ibm.com/case-studies/us-open",
            "https://www.ibm.com/sports/usopen",
            "https://newsroom.ibm.com/US-Open-AI-Tennis-Fan-Engagement",
            "https://newsroom.ibm.com/2024-08-15-ibm-and-the-usta-serve-up-new-and-enhanced-generative-ai-features-for-2024-us-open-digital-platforms",
        ]

        docs = [WebBaseLoader(url).load() for url in urls]
        docs_list = [item for sublist in docs for item in sublist]
        docs_list[0]
        
        MILVUS_HOST="milvus-service"
        MILVUS_PORT="19530"

        connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)
        app.logger.info('Connected to Milvus Host '+MILVUS_HOST)
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=0)
        doc_splits = text_splitter.split_documents(docs_list)
        app.logger.info('Splitting Text')
        app.logger.info('Text split into '+str(len(doc_splits))+' chunks')
        
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        app.logger.info('Getting embeddings')

        app.logger.info('Beginning vector store')
        vector_store = Milvus.from_documents(
            docs,
            embedding=embeddings,
            collection_name="agentic-rag",
            connection_args={"host": MILVUS_HOST, "port": MILVUS_PORT}
        )
        app.logger.info('Completed vector store')

        retriever = vectorstore.as_retriever()
        
        tools = [get_IBM_US_Open_context]

        system_prompt = """Respond to the human as helpfully and accurately as possible. You have access to the following tools: {tools}
Use a json blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).
Valid "action" values: "Final Answer" or {tool_names}
Provide only ONE action per $JSON_BLOB, as shown:"
```
{{
  "action": $TOOL_NAME,
  "action_input": $INPUT
}}
```
Follow this format:
Question: input question to answer
Thought: consider previous and subsequent steps
Action:
```
$JSON_BLOB
```
Observation: action result
... (repeat Thought/Action/Observation N times)
Thought: I know what to respond
Action:
```
{{
  "action": "Final Answer",
  "action_input": "Final response to human"
}}
Begin! Reminder to ALWAYS respond with a valid json blob of a single action.
Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation"""

        human_prompt = """{input}
{agent_scratchpad}
(reminder to always respond in a JSON blob)"""

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder("chat_history", optional=True),
                ("human", human_prompt),
            ]
        )

        prompt = prompt.partial(
            tools=render_text_description_and_args(list(tools)),
            tool_names=", ".join([t.name for t in tools]),
        )

        memory = ConversationBufferMemory()

        chain = (
            RunnablePassthrough.assign(
                agent_scratchpad=lambda x: format_log_to_str(x["intermediate_steps"]),
                chat_history=lambda x: memory.chat_memory.messages,
            )
            | prompt
            | llm
            | JSONAgentOutputParser()
        )
        
        agent_executor = AgentExecutor(
            agent=chain, tools=tools, handle_parsing_errors=True, verbose=True, memory=memory
        )

        agent_executor.invoke({"input": Query})
        
        content['result'] = "Success"

    
    else:
        content ['result'] = "Query Missing"
        
    return content


@tool
def get_IBM_US_Open_context(question: str):
    """Get context about IBM's involvement in the 2024 US Open Tennis Championship."""
    context = retriever.invoke(question)
    return context

@app.route('/healthz')
# Added healthcheck endpoint
def healthz():
    return "ok"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
