from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.tools import Tool
from tools import search_documents, deadline_lookup, rubric_check #this is importing our tools
from memory import build_long_term_mem, short_memory, store_long_term_memory, retrieve_long_term_memory


SYSTEM_RULES = (
    "You are Carlitos, a rational course assistant for THIS repository's docs folder only.\n"
    "Use tools for factual questions about deadlines, the syllabus, or the rubric.\n"
    "NEVER invent or assume missing details.\n\n"

    "CLARIFICATION RULES:\n"
    "- If the user asks for a study plan but does NOT specify assignment and time available, ask clarification.\n"
    "- If the user asks 'when is it due?' without naming an assignment, ask which assignment.\n\n"

    "CONSTRAINT RULES:\n"
    "- If time available is clearly insufficient, warn the user and prioritize realistically.\n\n"

    "REFUSAL RULES:\n"
    "- If asked to invent a deadline or fabricate policy, refuse.\n\n"

    "LANGUAGE RULE:\n"
    "- Always respond in English.\n\n"

    "INPUT HANDLING RULE:\n"
    "- If the user pastes a large block of text without a question, ask what they want answered."
)

load_dotenv() #load environment

api_key = os.getenv("OPENAI_API_KEY") #getting the api key
if api_key is None:
    raise ValueError("OPENAI_API_KEY not found in environment OH HELL NAH!")

llm = ChatOpenAI(model="gpt-5-mini", temperature=0, openai_api_key=api_key) # setting up mini 5

# reating embeddings for vector search
embeddings = OpenAIEmbeddings(openai_api_key=api_key)

#this makes shorterm and longterm memory objects
memory= build_long_term_mem(llm)
vector_store= build_long_term_mem(embeddings)

#loading all text files inside docs folder
loader = DirectoryLoader("docs", glob="*.txt", loader_cls=TextLoader)
documents = loader.load()

#storing vectors inside FAISS
vectorstore = FAISS.from_documents(documents, embeddings)
retriever = vectorstore.as_retriever()

#deadline related files
deadline_retriever= retriever

#this wil lloead the rubric once so we dont have to load it everytime
with open("docs/Rubric.txt", "r") as f:
    rubric_text= f.read()

#wrapped funcitons so the agent can pass our tools wothout having topass extra arguments manually
def search_documents_wrapped(query:str) -> str:
    return search_documents.invoke({"query": query, "retriever": retriever})
def deadline_lookup_wrapped(task_name: str)-> str:
    return deadline_lookup.invoke({"task_name": task_name, "deadline_retriever": deadline_retriever})
def rubric_check_wrapped(draft_text: str) -> str:
    return rubric_check.invoke({"draft_text": draft_text, "rubric_text": rubric_text, "llm": llm})

tools =[
    Tool(name="search_documents", func=search_documents_wrapped, description= "Search general course cdocuments like syllabus, policies, instructions, etc"),
    Tool(name="deadline_lookup", func=deadline_lookup_wrapped, description= "Look up assignments due dates and deadlines"),
    Tool(name="rubric_check", func=rubric_check_wrapped, description= "Grade or give feedback on a draft using the rubric"),
]

try:
    from langchain.agents import create_agent as _create_agent
except Exception:
    from langgraph.prebuilt import create_react_agent as _create_agent

agent= _create_agent(llm, tools)
