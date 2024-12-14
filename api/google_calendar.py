from ics import Calendar
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os

SCOPES = ["https://www.googleapis.com/auth/calendar.events", "https://www.googleapis.com/auth/calendar"]

class GoogleCalendar:
  def __init__(self):
    self.creds = None
    self.authenticate()
    self.service = build('calendar', 'v3', credentials=self.creds)
    self.calendar_id = 'primary'
    
  def authenticate(self):
    if os.path.exists("token.json"):
      self.creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not self.creds or not self.creds.valid:
      if self.creds and self.creds.expired and self.creds.refresh_token:
        self.creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        self.creds = flow.run_local_server(port=5000)
      with open("token.json", "w") as token:
        token.write(self.creds.to_json())

  def create_event(self, event):
    try:
      created_event = self.service.events().insert(
        calendarId=self.calendar_id,
        body=event
      ).execute()

      print(f"Event created: {created_event['summary']}")

      shortened_event = {
        'id': created_event['id'],
        'summary': created_event['summary'],
        'description': created_event['description'] if 'description' in created_event else '',
        'start': created_event['start'],
        'end': created_event['end']
      }
      return shortened_event
    
    except Exception as e:
      print(f"Exception occured while creating event: {e}")
  
  def create_events(self, ics_data):
    try:
      created_events = []

      calendar = Calendar(ics_data)

      for event in calendar.events:
        google_event = {
          'summary': event.name,
          'description': event.description,
          'location': event.location,
          'start': {
              'dateTime': event.begin.isoformat(),
          },
          'end': {
              'dateTime': event.end.isoformat(),
          },
        }

        created_events.append(self.create_event(google_event))
      return created_events

    except Exception as e:
      print(f"Exception occured while parsing events: {e}")
    