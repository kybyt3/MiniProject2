from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

load_dotenv() #load environment

api_key = os.getenv("OPENAI_API_KEY") #getting the api key
if api_key is None:
    raise ValueError("OPENAI_API_KEY not found in environment OH HELL NAH!")

llm = ChatOpenAI(model="gpt-5-mini", temperature=0, openai_api_key=api_key)#setting up mini 5


def dummy_tool(query): #dummy tool jsut to test
    return "This is a dummy response."

class SimpleAgent: # running the agent
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
    
    def run(self, query):
        tool_func = list(self.tools.values())[0]
        return tool_func(query)

tools = {"dummy_tool": dummy_tool}
agent = SimpleAgent(llm, tools)