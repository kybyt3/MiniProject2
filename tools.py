from langchain.tools import tool

@tool
def search_documents(query: str, retriever) -> str:
    """Search the provided local course files and return relevant content."""
    
    docs = retriever.invoke(query)

    if not docs:
        return "No relevant documents found."

    results = "\n\n".join([doc.page_content for doc in docs])
    return results

if __name__ == "__main__":
    print("Testing tool...")
    result = search_documents.invoke("When is Assignment 1 due?")
    print(result)
