from agent import agent #importing agent

if __name__ == "__main__":
    print("MiniProject2 Agent is running...\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Exiting agent...")
            break

        response = agent.run(user_input)
        print("\nAgent:", response)
        print()