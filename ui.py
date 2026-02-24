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

        self.chat_display= ScrolledText(# this si sto make a display area for the chat that is scrollable
            root,wrap=tk.WORD, state=tk.DISABLED)
        self.chat_display.pack(
            padx=10,
            paddy=10,
            fill=tk.BOTH,
            expand=True
        )
        #this is so we can paste the syllabus without breaking the terminal input
        self.input_box= tk.Text(root,height=4)
        self.input_box.pack(
            padx=10,
            paddy=(0,5),
            fill= tk.X
        )
        button_frame= tk.Frame(root) #evrything after this is for the buttons
        button_frame.pack(paddy=(0,10))

        self.send_button= tk.Button( #to send input
            button_frame,
            text= "SEND",
            command=self.send_message
        )
        self.clear_button= tk.Button(#for the clear chat button
            button_frame,
            text="CLEAR CHAT",
            command=self.clear_chat
        )




