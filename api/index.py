from flask import Flask
import openai
import requests
from icalendar import Calendar, Event
from datetime import datetime

app = Flask(__name__)

@app.route("/api/python")
def hello_world():
    return "<p>Hello, World!</p>"

app.run(debug=True)