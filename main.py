from agent import agent, vector_store, llm  # importing agent
from memory import retrieve_long_term_memory, short_memory
SYSTEM_RULES = (
    "You are Carlitos, a rational course assistant for THIS repository's docs folder only.\n"
    "Use tools for factual questions about deadlines, the syllabus, or the rubric.\n"
    "NEVER invent or assume missing details.\n\n"

    "CONSTRAINT / REALISM RULES (VERY IMPORTANT):\n"
    "- If the user’s time available is clearly insufficient for the request (example: '1 hour to prepare for the midterm' + 'complete schedule'), you MUST:\n"
    "  1) explicitly warn that the time is insufficient,\n"
    "  2) prioritize the highest-impact items,\n"
    "  3) provide a realistic micro-plan for the available time,\n"
    "  4) optionally suggest how many hours/days would be more realistic.\n"
    "- Do NOT pretend the user can fully prepare in an impossible timeframe.\n\n"

    "CLARIFICATION RULES (VERY IMPORTANT):\n"
    "- If the user asks for a study plan but does NOT specify the assignment/goal AND time available, you MUST ask:\n"
    "  1) which assignment/goal?\n"
    "  2) how many days available?\n"
    "  3) how many hours per day?\n"
    "  Do NOT generate a plan until you have these.\n"
    "- If the user asks 'when is it due?' or uses a pronoun ('it', 'that'), you MUST ask which assignment they mean.\n"
    "  Do NOT assume Assignment 1.\n\n"

    "REFUSAL RULES (VERY IMPORTANT):\n"
    "- If the user asks you to invent/fabricate a deadline or policy, you MUST refuse.\n"
    "- You may suggest telling them to check the syllabus/FAQ or propose a study plan timeline, but you cannot create a fake due date.\n\n"

    "LANGUAGE RULE:\n"
    "- Always respond in English.\n"
)

memory= short_memory(llm)

if __name__ == "__main__":
    print("Carlitos Agent is running...\n")
    
    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Exiting agent...")
            break

        if len(user_input) > 800 and "?" not in user_input: #this is for long input handling
            print(
            "\nCarlitos Agent: I received a large block of text. "
            "What specific question would you like me to answer about it?\n"
            )
            continue

        remember=  retrieve_long_term_memory(vector_store, user_input)
        messages= [("system", SYSTEM_RULES)]
        if remember:
            messages.append(("system", f"Long-term memory (may help): \n{remember}"))
        messages.append(("user", user_input))
        if memory.chat_memory.messages:
            messages.append(("system", "short-term memory(recent conversation):"))
            for m in memory.chat_memory.messages:
                role= "user" if m.type== "human" else "assistant"
                messages.append((role, m.content))
        messages.append(("user", user_input))

        result = agent.invoke({"messages": messages})
        final_answer = result["messages"][-1].content
        print("\nCarlitos Agent:", final_answer)
        print()

        #uodating short memory automatically
        memory.save_context({"input": user_input}, {"output": final_answer})