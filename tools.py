from langchain.tools import tool
from langchain_community.document_loaders import DirectoryLoader # built-in directory loader for documents
from langchain_community.document_loaders import TextLoader # to load .txt files
from langchain_openai import OpenAIEmbeddings # converts text from documents into vectors
from langchain_community.vectorstores import FAISS # actually stores document vectors for similarity search

# loads all text files
loader = DirectoryLoader("docs", glob="*.txt", loader_cls=TextLoader)
documents = loader.load()

# embeds text into vectors to retrieve and search
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(documents, embeddings)
retriever = vectorstore.as_retriever()

# search_documents tool: search provided local course files 
@tool
def search_documents(query: str) -> str:
    """Search the provided local course files and return relevant content."""
    docs = retriever.get_relevant_documents(query)
    results = "\n\n".join([doc.page_content for doc in docs])
    return results

if __name__ == "__main__":
    print("Testing tool...")
    result = search_documents.invoke("When is Assignment 1 due?")
    print(result)
