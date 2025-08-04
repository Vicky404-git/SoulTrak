#E:\Habit Tracker\SoulTrak\UI\serversoul.py
from flask import Flask, render_template, request, jsonify
import sys
import os
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ai_brian .run_brian import run_planner



app = Flask(__name__)  # This will automatically look in './templates/'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dash.html')

@app.route("/get_trak_data")
def get_trak_data():
    try:
        base_dir = os.path.abspath(os.path.dirname(__file__))  # current: UI/
        csv_path = os.path.join(base_dir, "..", "UI", "trak.csv")  # points to correct file
        df = pd.read_csv(csv_path)
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/ai')
def ai_page():
    return render_template('ai.html')



@app.route("/ai/with_ai")
def run_ai_route():
    index = int(request.args.get("index", 0))  # default to 0
    try:
        output = run_planner(index)  # your AI function
        return jsonify({"output": output})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/ask', methods=['POST'])
def ask_ai():
    data = request.get_json()
    user_input = data.get("message", "")
    if not user_input.strip():
        return jsonify({"response": "Please enter something."})

    response = run_planner(user_input)
    return jsonify({"response": response})

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/progress')
def progress():
    return render_template('progress.html')

if __name__ == '__main__':
    app.run(debug=True)
