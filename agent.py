from dotenv import load_dotenv
from tools import search_documents
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain.agents import initialize_agent, AgentType
from tools import search_documents, deadline_lookup, rubric_check #this is importing our tools

load_dotenv() #load environment

api_key = os.getenv("OPENAI_API_KEY") #getting the api key
if api_key is None:
    raise ValueError("OPENAI_API_KEY not found in environment OH HELL NAH!")

llm = ChatOpenAI(model="gpt-5-mini", temperature=0, openai_api_key=api_key) # setting up mini 5

# reating embeddings for vector search
embeddings = OpenAIEmbeddings(openai_api_key=api_key)

#loading all text files inside docs folder
loader = DirectoryLoader("docs", glob="*.txt", loader_cls=TextLoader)
documents = loader.load()

#storing vectors inside FAISS
vectorstore = FAISS.from_documents(documents, embeddings)
retriever = vectorstore.as_retriever()

#deadline related files
deadline_loader = DirectoryLoader("docs", glob="*deadline", loader_cls=TextLoader)
deadline_docs = deadline_loader.load()
deadline_store= FAISS.from_documents(deadline_docs, embeddings)
deadline_retriever= deadline_store.as_retriver()

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
    type(search_documents)(name="search_documents", func=search_documents_wrapped, description= search_documents.description),
    type(deadline_lookup)(name="deadline_lookup", func=deadline_lookup_wrapped, description= deadline_lookup.description),
    type(rubric_check)(name="rubric_check", func=rubric_check_wrapped, description= rubric_check.description),
]




agent = SimpleAgent(llm, retriever)