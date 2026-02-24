from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate


# search_documents tool: search provided local course files 
@tool
def search_documents(query: str, retriever) -> str:
    """Search the provided local course files and return relevant content."""
    docs = retriever.invoke(query)
    if not docs:
        return "No relevant documents found."
    results = "\n\n".join([doc.page_content for doc in docs])
    return results

@tool
def deadline_lookup(task_name: str, deadline_retriever) -> str:
    """Returns due dates from deadline documents."""
    
    docs = deadline_retriever.invoke(task_name)
    if not docs:
        return "No deadline information found."
    results = "\n\n".join([doc.page_content for doc in docs])
    return results


@tool
def rubric_check(draft_text: str, rubric_text: str, llm) -> str:
    """Evaluates a given draft using rubric.txt"""

    prompt = ChatPromptTemplate.from_template("""
    You are a grader. Evaluate the following submission against the rubric.

    Rubric:
    {rubric}
    Submission:
    {submission}

    Provide specific feedback and a score for each rubric criterion.
    """)
    chain = prompt | llm
    response = chain.invoke({
        "rubric": rubric_text,
        "submission": draft_text
    })
    return response.content