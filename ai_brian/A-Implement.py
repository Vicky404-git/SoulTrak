from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()
API = os.getenv('API')  # .env must have a line like: API=your_groq_api_key

# Read data
df = pd.read_csv("trak.csv")
print(df.head())

# Create prompt (optional customization)
Custom_Prompt = '''You are a personal AI tracker assistant. Help user analyze or plan activities based on the CSV log.'''

# Initialize Groq LLM
llm = ChatGroq(
    temperature=0,
    groq_api_key=API,
    model_name="llama3-70b-8192"  # Correct model name, not "llama-3.3-70b-versatile"
)

# Ask something simple
prompt = f"""You are a personal AI tracker assistant. 
Help user analyze or plan activities based on the CSV log.
Here's my activity log for today:
{df.tail(10).to_string(index=False)}

Give me feedback and how I can improve tomorrow."""
response = llm.invoke(prompt)
print(response.content)
