import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading

from agent import agent, vector_store, SYSTEM_RULES
from memory import retrieve_long_term_memory

class CarlitosAgent: #this is to mange the UI window
    def __init__(self, root):
        self.root= root
        root.title("Carlitos- AI Course Assistant")
        root.geometry("900x600")

        bottom_frame = tk.Frame(root)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        self.input_box = tk.Text(bottom_frame, height=4)
        self.input_box.pack(fill=tk.X, pady=(0, 8))

        button_frame = tk.Frame(bottom_frame)
        button_frame.pack(fill=tk.X)

        self.send_button = tk.Button(button_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=(0, 8))

        self.clear_button = tk.Button(button_frame, text="Clear Chat", command=self.clear_chat)
        self.clear_button.pack(side=tk.LEFT)

        self.chat_display= ScrolledText(# this si sto make a display area for the chat that is scrollable
            root,wrap=tk.WORD, state=tk.DISABLED)
        self.chat_display.pack(
            padx=10,
            pady=10,
            fill=tk.BOTH,
            expand=True
        )

    def append_chat(self, text): #APPENDS THE TEXT TO THE CHAT
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, text)
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def clear_chat(self):#this will erase UI chat window not the entire memory
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state=tk.DISABLED)
    def send_message(self):
        user_input= self.input_box.get("1.0", tk.END).strip()
        self.input_box.delete("1.0", tk.END)

        if not user_input:
            return #this will ignore empty messages
        
        self.append_chat(f"You:\n{user_input}\n\n")
        self.append_chat("Carlitos is thinking...\n\n")

        threading.Thread(
            target=self.process_message, #making this gfunction after for background agent processing
            args=(user_input,),
            daemon= True
        ).start()

    def process_message(self, user_input):
        if len(user_input)> 800 and "?" not in user_input:
            response= (
                "I received a large block of text. "
                "What specific question would you like me to answer about it?"
            )
        else:
            remember = retrieve_long_term_memory(vector_store, user_input)
            messages = [("system", SYSTEM_RULES)]

            if remember:
                messages.append(("system", f"Long-term memory:\n{remember}"))
            messages.append(("user", user_input))
            try:
                result = agent.invoke({"messages": messages})
                response = result["messages"][-1].content
            except Exception as e:
                response = f"Error: {str(e)}"

        self.root.after(0, self.display_response, response)

    def display_response(self, response):#will display agent response
        self.chat_display.config(state=tk.NORMAL)
        content= self.chat_display.get("1.0", tk.END)
        content= content.replace("Carlitos is thinking...\n\n","")
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.insert(tk.END, content)
        self.chat_display.config(state=tk.DISABLED)

        self.append_chat(f"Carlitos:\n{response}\n\n")

if __name__== "__main__":
    root= tk.Tk()
    app= CarlitosAgent(root)
    root.mainloop()