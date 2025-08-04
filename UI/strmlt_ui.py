
# ui/streamlit_ui.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from ai_brian import prompt_templates as pt
from ai_brian import csvpln

def run_ui():
    st.title("🧠 SoulTrak AI Planner")
    st.write("Upload your `trak.csv` file to get insights from your logs.")

    uploaded_file = st.file_uploader("Upload CSV Log", type=["csv"])

    prompt_choice = st.selectbox("Choose a prompt", list(pt.PROMPT_OPTIONS.keys()))

    if uploaded_file and st.button("🧠 Generate Insights"):
        csv_data = uploaded_file.getvalue().decode("utf-8")
        selected_prompt = pt.PROMPT_OPTIONS[prompt_choice]
        response = csvpln.generate_output(selected_prompt, csv_data)
        st.success("✅ Done!")
        st.markdown("### 💬 AI Feedback:")
        st.write(response)

if __name__ == "__main__":
    run_ui()
