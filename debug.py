# debug.py
import os
import sys

def check_environment():
    print("🔍 Checking Environment Variables...")
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("API")
        if api_key:
            print("  ✅ API Key found in .env")
        else:
            print("  ❌ API Key missing! Please add API='your_key' to your .env file.")
    except Exception as e:
         print(f"  ❌ Error loading dotenv: {e}")

def check_data_file():
    print("\n🔍 Checking Data Files...")
    import pandas as pd
    
    # Check common locations for the tracker CSV
    paths = ["trak.csv", "UI/trak.csv", "../UI/trak.csv"]
    found = False
    
    for path in paths:
        if os.path.exists(path):
            print(f"  ✅ Found data file at: {path}")
            try:
                df = pd.read_csv(path)
                print(f"  ✅ Successfully loaded {len(df)} rows from {path}")
                found = True
                break
            except Exception as e:
                print(f"  ❌ Error reading {path}: {e}")
                
    if not found:
        print("  ❌ trak.csv not found. Core Flask routes and Pandas functions will fail.")
        print("  💡 Fix: Run 'echo \"timestamp,date,time,activity_type,task,duration_min,intensity,status,notes\" > UI/trak.csv'")

def check_imports():
    print("\n🔍 Checking Core Modules...")
    modules = ['flask', 'pandas', 'langchain_groq', 'matplotlib', 'dotenv']
    for mod in modules:
        try:
            __import__(mod)
            print(f"  ✅ Module '{mod}' loaded successfully.")
        except ImportError as e:
            print(f"  ❌ Missing module '{mod}': {e}")

def check_ai_connection():
    print("\n🔍 Testing AI Connection...")
    try:
        # Import llm directly from your ai_brian package
        from ai_brian.csvpln import llm
        print("  ⏳ Pinging Groq API...")
        response = llm.invoke("Respond with the exact phrase 'Connection successful' if you receive this.")
        print(f"  ✅ AI Response: {response.content}")
    except Exception as e:
        print(f"  ❌ AI Connection failed: {e}")

if __name__ == "__main__":
    print("=================================")
    print("    SOULTRAK SYSTEM DEBUGGER     ")
    print("=================================\n")
    check_imports()
    check_environment()
    check_data_file()
    check_ai_connection()
    print("\n=================================")
    print("       DEBUGGING COMPLETE        ")
    print("=================================")
