import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# ...existing code...
from flask import Flask, request, jsonify
from src.prompt import prompt
from src.llm import llm
# ...existing code...
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from flask_cors import CORS


app = Flask(__name__)
CORS(app) 

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
rag_chain = (
    prompt
    | llm
)

@app.route('/')
def index():
    return "Chatbot is running"
@app.route('/api/chat/completions', methods=['POST'])
def chat():
    try:
        # Parse the input JSON
        data = request.json
        messages = data.get("messages", [])

        # Convert messages to HumanMessage and AIMessage objects
        chain_messages = []
        for msg in messages:
            if msg["role"] == "user":
                chain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                chain_messages.append(AIMessage(content=msg["content"]))
            elif msg["role"] == "system":
                chain_messages.append(SystemMessage(content=msg["content"]))

        response = rag_chain.invoke({"messages": chain_messages})
        print("Response generated:", response)
        # Return the AI's response
        response_main = {
        "choices": [
            {
                "index": 0,
                "logprobs": None,
                "finish_reason": "stop",
                "message": {
                    "content": response.content,
                    "role": "assistant"
                }
            }
        ]
    }
        return jsonify(response_main), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
