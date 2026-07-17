# ai_brain/csvpln.py

import pandas as pd
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

llm = ChatGroq(
    temperature=0,
    groq_api_key=os.getenv("API"),
    model_name="llama-3.1-8b-instant"
)

CACHE_FILE = os.path.join(os.path.dirname(__file__), "..", "UI", "ai_cache.csv")

def get_cached_response(prompt_key: str, latest_task_time: str) -> str:
    """Checks if we already have a response for this exact state."""
    if not os.path.exists(CACHE_FILE):
        return None
    try:
        cache_df = pd.read_csv(CACHE_FILE)
        # Match the exact prompt category AND the exact timestamp of the last logged task
        match = cache_df[
            (cache_df['prompt_choice'] == prompt_key) & 
            (cache_df['latest_task_time'] == str(latest_task_time))
        ]
        if not match.empty:
            return match.iloc[-1]['response']
    except Exception:
        return None
    return None

def save_to_cache(prompt_key: str, latest_task_time: str, response: str):
    """Saves the fresh response to a separate CSV cache."""
    new_row = {
        "cache_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "prompt_choice": prompt_key,
        "latest_task_time": str(latest_task_time),
        "response": response
    }
    
    if os.path.exists(CACHE_FILE):
        cache_df = pd.read_csv(CACHE_FILE)
        cache_df = pd.concat([cache_df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        cache_df = pd.DataFrame([new_row])
        
    cache_df.to_csv(CACHE_FILE, index=False)

def generate_output(selected_prompt: str, df: pd.DataFrame, prompt_key: str = "Custom") -> str:
    # 1. Figure out the timestamp of the latest task in the tracker
    if not df.empty and 'timestamp' in df.columns:
        latest_task_time = str(df.iloc[-1]['timestamp'])
    else:
        latest_task_time = "empty_log"

    # 2. Check the cache to see if we already generated this request
    cached = get_cached_response(prompt_key, latest_task_time)
    if cached:
        return "[⚡ Loaded from Cache]\n\n" + cached

    # 3. If no cache exists, generate a new response
    recent_df = df.tail(50)
    activity_log = "\n".join(recent_df.astype(str).apply(" | ".join, axis=1).tolist())

    filled_prompt = selected_prompt.replace("{{context}}", activity_log)
    prompt = PromptTemplate.from_template(filled_prompt)
    chain = prompt | llm
    
    response_content = chain.invoke({}).content
    
    # 4. Save the fresh response to the cache for next time
    save_to_cache(prompt_key, latest_task_time, response_content)
    
    return response_content
