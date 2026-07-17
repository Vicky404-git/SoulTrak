# ai_brain/csvpln.py

import pandas as pd
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    temperature=0,
    groq_api_key=os.getenv("API"),
    model_name="llama-3.1-8b-instant"
)

def generate_output(selected_prompt: str, df: pd.DataFrame) -> str:
    # 1. Limit to the last 50 entries to avoid exceeding token limits
    recent_df = df.tail(50)
    
    # 2. Format the dataframe into a readable string for the prompt
    activity_log = "\n".join(recent_df.astype(str).apply(" | ".join, axis=1).tolist())

    # 3. Inject context into the prompt
    filled_prompt = selected_prompt.replace("{{context}}", activity_log)

    # 4. Invoke the LangChain process
    prompt = PromptTemplate.from_template(filled_prompt)
    chain = prompt | llm
    
    # 5. Extract and return just the text content
    response = chain.invoke({})
    return response.content
