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

@app.route("/api/python", methods=['POST'])
def hello_world():
    openai.api_key = OPENAI_API_KEY
    
    try:
        data = request.get_json()
        prompt = data['prompt']

        today = datetime.now()

        formatted_date = today.strftime("%A, %B %d, %Y")

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are an assistant that generates ICS formatted calendar events. You only respond with the ICS output. Today is {formatted_date}. Respond in EST time."},
                {"role": "user", "content": f"Generate an ICS event for this request: {prompt}"}
            ]
        )
        ics_data = response.choices[0].message.content
        print(ics_data)

    except Exception as e:
        return {"error": f"Failed to get ICS data from OpenAI: {str(e)}"}
    
    try:
        calendar = Calendar(ics_data)

        for event in calendar.events:

            google_event = {
                'summary': event.name,
                'description': event.description,
                'location': event.location,
                'start': {
                    'dateTime': event.begin.isoformat(),  # Google Calendar API expects ISO 8601 format
                    #'timeZone': 'EST'
                },
                'end': {
                    'dateTime': event.end.isoformat(),
                    #'timeZone': 'EST'
                },
            }

            post_event(google_event)

    except Exception as e:
        return {"error": f"Invalid ICS data: {str(e)}"}
    
    return Response("", status=200)

def post_event(event):
    print('event', event)
    service = build('calendar', 'v3', credentials=creds)
    calendar_id = 'primary'
    try:
        created_event = service.events().insert(
            calendarId=calendar_id,
            body=event
        ).execute()
        print(f"Event created: {created_event['summary']}")
    except Exception as e:
        print(f"An error occurred: {e}")

app.run(debug=True)
