# 🧠 SoulTrak — Your AI-Powered Life Planner

**SoulTrak** is a habit and life-tracking tool that uses AI to provide you with daily feedback, time management advice, and personalized motivation. Built using **Flask**, **Python**, and basic **HTML/CSS**, it's designed to help you reflect and improve—one day at a time.

---

## 🌟 Features

- 📊 **Daily/Weekly Logs** – Track your routines and activities
- 🤖 **AI Feedback** – Get personalized tips, analysis & motivation
- 🔁 **Habit Tracking** – Simple UI for updating your progress
- 🎯 **Productivity Coach** – Built-in prompts to reflect & plan
- 💡 **Dark + Light Mode** – Switch themes based on your vibe

---

## 🚀 Getting Started

### 1. Clone this Repo

```bash
git clone https://github.com/your-username/soultrak.git
cd soultrak
```
### 2. Create a Virtual Environment (optional but recommended)
``` bash
python -m venv trak
trak\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt

```

### 4. Run the App
```bash
cd UI
python serversoul.py

```

Then visit: http://localhost:5000

<hr>

📁 Folder Structure
```php
SoulTrak/
│
├── UI/                   # Flask frontend (HTML/CSS/JS)
│   ├── templates/        # Jinja2 HTML templates
│   ├── static/           # Custom stylesheets
│   └── serversoul.py     # Flask main server
│
├── ai_brain/             # AI module logic
│   ├── csvpln.py         # Data parsing and planner
│   ├── prompt_templates.py
│   └── run_brian.py      # Runs AI with selected prompt
│
├── trak.csv              # Your habit tracking data
├── README.md             # You're reading it!
└── .gitignore

```