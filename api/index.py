from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import openai
import requests
from icalendar import Calendar, Event
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
CORS(app)

@app.route("/api/python", methods=['POST'])
def hello_world():
    openai.api_key = OPENAI_API_KEY
    
    try:
        data = request.get_json()
        print(data)
        prompt = data['prompt']

        # response = openai.chat.completions.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {"role": "system", "content": "You are an assistant that generates ICS formatted calendar events."},
        #         {"role": "user", "content": f"Generate an ICS event for this request: {prompt}"}
        #     ]
        # )
        # ics_data = response.choices[0].message.content
        # print(ics_data)

        ics_data = 'BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Your Assistant//EN\nBEGIN:VEVENT\nDTSTAMP:20211211T000000Z\nUID:1234567890\nDTSTART:20241213T190000\nSUMMARY:Dinner\nEND:VEVENT\nEND:VCALENDAR'

    except Exception as e:
        return {"error": f"Failed to get ICS data from OpenAI: {str(e)}"}
    
    try:
        calendar = Calendar.from_ical(ics_data)

    except Exception as e:
        return {"error": f"Invalid ICS data: {str(e)}"}

app.run(debug=True)