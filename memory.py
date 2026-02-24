import os
from typing import List
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain.tools import tool
from langchain_classic.memory import ConversationSummaryBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.vectorstores import Chroma



# implementing short-term memory
memory = ConversationSummaryBufferMemory(
    llm=ChatOpenAI(model="gpt-5-mini", temperature=0.7),
    max_token_limit=500,
    return_messages=True
)

embeddings = OpenAIEmbeddings()

vector_store = Chroma(
    persist_directory="./student_memory",
    embedding_function=embeddings
)

# storing long term memory
def store_long_term_memory(text: str):
    vector_store.add_texts([text])
    vector_store.persist()

# retrieving long term memory
def retrieve_long_term_memory(query: str, k: int = 3) -> str:
    docs = vector_store.similarity_search(query=query, k=k)
    return "\n".join([doc.page_content for doc in docs])


