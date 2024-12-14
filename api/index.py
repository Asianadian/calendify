from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import openai
import requests
#from icalendar import Calendar, Event
from datetime import datetime
from dotenv import load_dotenv
import os
from ics import Calendar, Event
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from caldav import DAVClient
import pytz
from llm import LLM
from google_calendar import GoogleCalendar

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

SCOPES = ["https://www.googleapis.com/auth/calendar.events", "https://www.googleapis.com/auth/calendar"]

creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists("token.json"):
  creds = Credentials.from_authorized_user_file("token.json", SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
  if creds and creds.expired and creds.refresh_token:
    creds.refresh(Request())
  else:
    flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json", SCOPES
    )
    creds = flow.run_local_server(port=5000)
  # Save the credentials for the next run
  with open("token.json", "w") as token:
    token.write(creds.to_json())

print('done')
app = Flask(__name__)
CORS(app)

llm = LLM(OPENAI_API_KEY)
google_calendar = GoogleCalendar()

@app.route("/api/python", methods=['POST'])
def create_events_from_prompt():
    openai.api_key = OPENAI_API_KEY
    
    try:
        data = request.get_json()
        prompt = data['prompt']

    except Exception as e:
        return {"error": f"Failed to get request data: {str(e)}"}
    
    ics_data = llm.create_event_prompt(prompt)

    added_events = google_calendar.create_events(ics_data)
    
    return jsonify(added_events)

@app.route("/api/python", methods=['DELETE'])
def delete_event_from_prompt():
    openai.api_key = OPENAI_API_KEY
    
    try:
        data = request.get_json()
        prompt = data['prompt']
        events = data['events']

        today = datetime.now()

        formatted_date = today.strftime("%A, %B %d, %Y")

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are an assistant that determines if a description matches anything in the prompt. You only respond with the ICS output. Today is {formatted_date}. Respond in EST time."},
                {"role": "user", "content": f"Generate an ICS event for this request: {prompt}"}
            ]
        )
        ics_data = response.choices[0].message.content
        print(ics_data)

    except Exception as e:
        return {"error": f"Failed to get ICS data from OpenAI: {str(e)}"}
    
    try:
        ...

    except Exception as e:
        return {"error": f"Invalid ICS data: {str(e)}"}
    
    return jsonify(events)
app.run(debug=True)
