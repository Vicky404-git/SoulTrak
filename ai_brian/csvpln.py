#SoulTrak/ai_brain/csvpln.py

import pandas as pd
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable
import os
from dotenv import load_dotenv


load_dotenv()

llm = ChatGroq(
    temperature=0,
    groq_api_key=os.getenv("API"),
    model_name="llama3-70b-8192"
)

def generate_output(selected_prompt: str) -> str:
    df = pd.read_csv(r"E:\Habit Tracker\SoulTrak\UI\trak.csv")
    activity_log = "\n".join(df.astype(str).apply(" | ".join, axis=1).tolist())

    filled_prompt = selected_prompt.replace("{{context}}", activity_log)

    prompt = PromptTemplate.from_template(filled_prompt)
    chain: Runnable = prompt | llm
    return chain.invoke({})
