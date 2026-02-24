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


class SimpleAgent: #running the agent
    def __init__(self, llm, retriever):
        self.llm = llm
        self.retriever = retriever
    
    def run(self, query):
        # calling the search_documents tool with retriever
        return search_documents.invoke({
            "query": query,
            "retriever": self.retriever
        })


agent = SimpleAgent(llm, retriever)