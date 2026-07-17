# serversoul.py
from flask import Flask, render_template, request, session, redirect, url_for
import pandas as pd
import os
import sys

base_dir = os.path.abspath(os.path.dirname(__file__))
# Check if running from app subdirectory or root, adjusting path to match SoulTrak folder
sys.path.append(os.path.join(base_dir, "..")) 

from ai_brian import csvpln
from ai_brian.prompt_templates import PROMPT_OPTIONS

app = Flask(__name__)
app.secret_key = "supersecret"

@app.context_processor
def inject_theme():
    theme = session.get("theme", "solo")
    return dict(theme=theme)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dash.html")

@app.route("/progress")
def progress():
    return render_template("progress.html")

@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        chosen_theme = request.form.get("theme", "solo")
        session["theme"] = chosen_theme
        return redirect(url_for("settings"))
    return render_template("settings.html")

@app.route("/ai", methods=["GET", "POST"])
def ai_page():
    # Looks for trak.csv in the same directory as serversoul.py or UI folder
    csv_path = os.path.join(base_dir, "trak.csv")
    if not os.path.exists(csv_path):
        csv_path = os.path.join(base_dir, "..", "UI", "trak.csv")

    df = None
    try:
        df = pd.read_csv(csv_path)
        table_html = df.tail(10).to_html(classes="table", index=False)
    except Exception as e:
        table_html = f"<p class='error'>Error loading CSV: {e}</p>"

    ai_feedback = None

    if request.method == "POST" and df is not None:
        prompt_choice = request.form.get("prompt_choice")
        user_custom_input = request.form.get("user_input", "").strip()

        # Handle Template choice vs Custom chat question
        if prompt_choice in PROMPT_OPTIONS:
            selected_prompt = PROMPT_OPTIONS[prompt_choice]
        elif user_custom_input:
            # Build a custom template on the fly using the user's question
            selected_prompt = f"{user_custom_input}\n\nHere is my context log:\n{{{{context}}}}"
        else:
            selected_prompt = PROMPT_OPTIONS["Daily Feedback"]

        try:
            cache_key = prompt_choice if prompt_choice in PROMPT_OPTIONS else "Custom"
            ai_feedback = csvpln.generate_output(selected_prompt, df, prompt_key=cache_key)
        except Exception as e:
            ai_feedback = f"Error generating insights: {str(e)}"

    return render_template(
        "ai.html", 
        table_html=table_html, 
        ai_feedback=ai_feedback, 
        prompt_keys=list(PROMPT_OPTIONS.keys())
    )

if __name__ == "__main__":
    app.run(debug=True)
