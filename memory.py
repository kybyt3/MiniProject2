from langchain_classic.memory import ConversationSummaryBufferMemory
from langchain_community.vectorstores import Chroma



# implementing short-term memory
def short_memory(llm):
    return ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=500,
    return_messages= True
    )
# storing long term memory
def build_long_term_mem(embeddings):
    return Chroma(
        persist_directory="./user_memory",
        embedding_function= embeddings
    )
def store_long_term_memory(vector_store, text: str):
    vector_store.add_texts([text])
    vector_store.persist()

# retrieving long term memory
def retrieve_long_term_memory(vector_store, query: str, k: int = 3) -> str:
    docs = vector_store.similarity_search(query=query, k=k)
    if not docs:
        return ""
    return "\n".join([doc.page_content for doc in docs])


