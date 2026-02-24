from langchain.tools import tool
from langchain_community.document_loaders import DirectoryLoader # built-in directory loader for documents
from langchain_community.document_loaders import TextLoader # to load .txt files
from langchain_openai import OpenAIEmbeddings # converts text from documents into vectors
from langchain_community.vectorstores import FAISS # actually stores document vectors for similarity search
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from agent import llm


# loads all text files
loader = DirectoryLoader("docs", glob="*.txt", loader_cls=TextLoader)
documents = loader.load()

# embeds text into vectors to retrieve and search
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(documents, embeddings)
retriever = vectorstore.as_retriever()

deadline_loader = DirectoryLoader("docs", glob="*deadline*", loader_cls=TextLoader)
deadline_docs = deadline_loader.load()
deadline_store = FAISS.from_documents(deadline_docs, embeddings)
deadline_retriever = deadline_store.as_retriever()


# search_documents tool: search provided local course files 
@tool
def search_documents(query: str) -> str:
    """Search the provided local course files and return relevant content."""
    docs = retriever.invoke(query)
    results = "\n\n".join([doc.page_content for doc in docs])
    return results

@tool
def deadline_lookup(task_name:str ) ->str:
    """Returns due dates from a file."""
    docs = deadline_retriever.invoke(task_name)
    results = "\n\n".join([doc.page_content for doc in docs])
    return results

@tool
def rubric_check(draft_text:str ) ->str:
    """Evaluates a given draft using rubric.txt"""
    with open("docs/Rubric.txt") as f:
        rubric = f.read()
    prompt = ChatPromptTemplate.from_template("""You are a grader. Evaluate the following submission against the rubric.
    
    Rubric:
    {rubric}
    
    Submission:
    {submission}
    
    Provide specific feedback and a score for each rubric criterion.""")

    chain = prompt | llm 
    response = chain.invoke({"rubric": rubric, "submission": draft_text})
    return response.content # return result
