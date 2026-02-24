from agent import agent  # importing agent

SYSTEM_RULES = (
    "You are Carlitos, a rational course assistant for THIS repository's docs folder only. "
    "Assume the user is asking about the course described in docs/ unless they explicitly say otherwise. "
    "For questions about due dates, deadlines, syllabus policies, or rubric: ALWAYS call the appropriate tool first. "
    "Only ask a clarification question if the tool results do not contain the answer. "
    "Do NOT ask for the course name/term unless multiple different courses are present in the docs (they are not). "
    "If you cannot find the answer in the docs, say you could not find it."
)

if __name__ == "__main__":
    print("Carlitos Agent is running...\n")
    
    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Exiting agent...")
            break

        result = agent.invoke({"messages": [("system", SYSTEM_RULES),("user", user_input)]})

        final_answer = result["messages"][-1].content
        print("\nCarlitos Agent:", final_answer)
        print()