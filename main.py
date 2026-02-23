from dotenv import load_dotenv
import os

load_dotenv() #this will laod the variables from .env

api_key = os.getenv("OPENAI_API_KEY")#this will get the API key

print("API key loaded successfully!") # this si to make sure our api loaded successfully