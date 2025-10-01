#SoulTrak\app\trak_utils.py

import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


#===================================================================================================================

def view_streak():
    if not os.path.exists("trak.csv"):
        print("No data found.")
        return

    df = pd.read_csv("trak.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date

    # Filter only ✅ days
    valid_days = df[df["status"] == "✅"]
    valid_days = valid_days.groupby("date").first().reset_index()
    valid_days = valid_days.sort_values(by="date")

    from datetime import timedelta, date
    today = date.today()

    current_streak = 0
    max_streak = 0
    prev_date = None

    for _, row in valid_days.iterrows():
        current_date = row["date"]

        if prev_date is None:
            current_streak = 1
        elif (current_date - prev_date) == timedelta(days=1):
            current_streak += 1
        else:
            current_streak = 1  # Streak reset

        max_streak = max(max_streak, current_streak)
        prev_date = current_date

    if valid_days["date"].max() == today:
        print(f"🔥 Current streak: {current_streak} days")
    else:
        print(f"🛑 Streak ended. Last streak was {current_streak} days.")
    
    print(f"🏆 Max streak: {max_streak} days")

#===================================================================================================================

def plot_weekly_act():
    if not os.path.exists("trak.csv"):
        print("No data found.")
        return

    df = pd.read_csv("trak.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date

    # Filter only ✅ entries
    df = df[df["status"] == "✅"]

    # Get today's date and generate last 7 dates
    today = datetime.now().date()
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]

    # Group and sum duration per day
    daily_summary = df.groupby("date")["duration_min"].sum()

    # Fill missing dates with 0
    durations = [daily_summary.get(day, 0) for day in last_7_days]
    dates_str = [day.strftime("%a\n%d-%b") for day in last_7_days]  # For better x labels

    # Plot bar chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(dates_str, durations, color='skyblue')
    plt.title("🗓️ Last 7 Days – Activity Duration (Minutes)", fontsize=14)
    plt.xlabel("Date")
    plt.ylabel("Duration (min)")

    # Add value labels on top of each bar
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{int(yval)}', ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.show()



#===================================================================================================================

