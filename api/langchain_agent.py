from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentExecutor
from llm import LLM
from google_calendar import GoogleCalendar
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

llm = LLM(OPENAI_API_KEY)
google_calendar = GoogleCalendar()

def create_events(prompt):
  ics_data = llm.create_event_prompt(prompt)
  added_events = google_calendar.create_events(ics_data)
  print(added_events)
  return added_events
  ...

def delete_events(prompt):
  print("delete", prompt)  
  ...

create_event_tool = Tool(
  name='CreateEvents',
  func=create_events,
  return_direct=True,
  description='Use this for scheduling events'
)

delete_event_tool = Tool(
  name='DeleteEvents',
  func=delete_events,
  description='Use this for deleting events'
)

tools = [create_event_tool, delete_event_tool]

class CustomAgent(AgentExecutor):
  def _call_tool(self, tool_name, tool_input):
    if tool_name == "CreateEvents":
      return create_events(tool_input)
    elif tool_name == "DeleteEvents":
      return delete_events(tool_input)
    else:
      return super()._call_tool(tool_name, tool_input)

  def run(self, prompt):
    response = super().run(prompt)
    return response

class LangChainAgent:
  def __init__(self, api_key):
    os.environ["OPENAI_API_KEY"] = api_key
    self.llm = ChatOpenAI(temperature=0.1)
    self.agent = initialize_agent(tools, self.llm, agent="zero-shot-react-description", verbose=True, return_direct=True)

  def run(self, prompt):
    a = self.agent.run(prompt)
    print(a)
    return a


  
