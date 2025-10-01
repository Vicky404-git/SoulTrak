
# serversoul.py
from flask import Flask, render_template, request, session, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "supersecret"  # needed for session storage

# ---- AI BRAIN placeholder ----
def run_ai_brain(text):
    return f"AI_BRAIN says: {text}"

# ---- Inject theme into all templates ----
@app.context_processor
def inject_theme():
    theme = session.get("theme", "solo")  # default = solo
    return dict(theme=theme)

# ---- ROUTES ----
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
    base_dir = os.path.abspath(os.path.dirname(__file__))
    csv_path = os.path.join(base_dir, "..", "UI", "trak.csv")

    # Load CSV into HTML table
    try:
        df = pd.read_csv(csv_path)
        table_html = df.to_html(classes="table", index=False)

    except Exception as e:
        table_html = f"<p class='error'>Error loading CSV: {e}</p>"

    ai_feedback = None
    if request.method == "POST":
        user_input = request.form.get("user_input", "")
        ai_feedback = run_ai_brain(user_input)

    return render_template("ai.html", table_html=table_html, ai_feedback=ai_feedback)

# ---- RUN ----
if __name__ == "__main__":
    app.run(debug=True)
