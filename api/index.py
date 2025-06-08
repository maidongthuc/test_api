from flask import Flask
from langchain_google_genai import ChatGoogleGenerativeAI
app = Flask(__name__)

@app.route('/')
def home():
    return 'hello Ký'

@app.route('/about')
def about():
    return 'About'