from agent import agent, vector_store, llm, SYSTEM_RULES # importing agent
from memory import retrieve_long_term_memory, short_memory

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