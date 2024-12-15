import openai
from datetime import datetime
import time

def datetime_information():
  today = datetime.now()
  info = f' Today is {today.strftime("%A, %B %d, %Y")}. The timezone is {time.tzname[1]}.'
  return info

class LLM:
  def __init__(self, api_key):
    openai.api_key = api_key

  def create_event_prompt(self, prompt):
    response = openai.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": f"You are an assistant that generates ICS formatted calendar events. You only respond with the ICS output. {datetime_information()}"},
        {"role": "user", "content": f"Generate an ICS event for this request: {prompt}"}
      ]
    )
    ics_data = response.choices[0].message.content
    return ics_data
  
  def delete_event_prompt(self, prompt):
    response = openai.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": f"You are an assistant that returns calendar event IDs that match a description. You only respond with the IDs in a list in JSON. {datetime_information()}"},
        {"role": "user", "content": f"The events are as follows:{prompt} \nGenerate an ICS event for this request: {prompt}"}
      ]
    )
    ics_data = response.choices[0].message.content
    return ics_data
