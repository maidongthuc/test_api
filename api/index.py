import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from flask import Flask, request, jsonify
from src.retrieval import retriever, retriever_2
from langchain_core.runnables import RunnablePassthrough
from src.prompt import prompt
from src.llm import llm
from langchain.schema import HumanMessage, AIMessage
from flask_cors import CORS


app = Flask(__name__)
CORS(app) 

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
rag_chain = (
    {
        # Extract the content from the first HumanMessage in the input list
        "context": (lambda x: x[0].content) | retriever | format_docs,
        "blog": (lambda x: x[0].content) | retriever_2 | format_docs,
        # Pass the input list directly as the question for the prompt template
        "question": RunnablePassthrough(),
    }
    | prompt
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

        response = rag_chain.invoke(chain_messages)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)