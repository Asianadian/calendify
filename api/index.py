from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from llm import LLM
from google_calendar import GoogleCalendar
from langchain_agent import LangChainAgent

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
CORS(app)

llm = LLM(OPENAI_API_KEY)
agent = LangChainAgent(OPENAI_API_KEY)
google_calendar = GoogleCalendar()

@app.route("/api/langchain", methods=['POST'])
def create_events_from_prompt():
    try:
        
        data = request.get_json()
        prompt = data['prompt']

        added_events = agent.run(prompt)

        return jsonify(added_events)

    except Exception as e:
        return {"error": f"Failed to create events: {str(e)}"}

app.run(debug=True)
