#SoulTrak\app\data_manage.py

import pandas as pd
import os
import matplotlib.pyplot as plt
import trak_utils as t

data = {
    "timestamp": [],
    "date": [],
    "time": [],
    "activity_type": [],
    "task": [],
    "duration_min": [],
    "intensity": [],
    "status": [],
    "notes": []
}


df = pd.DataFrame(data)


def trak():
    from datetime import datetime
    now = datetime.now()
    date = now.strftime("%d/%m/%Y")
    time = now.strftime("%H:%M:%S")

    print("__________Hourly Trak___________")
    print("__________Add Trak___________")

    activity_type = input("What did you do?\n")
    task = input("Describe the task in short:\n")
    duration_min = float(input("How many minutes?\n"))

    # Intensity mapping
    intensity_map = {1: "Low", 2: "Medium", 3: "High"}
    intensity_input = int(input("Intensity? (1=Low, 2=Medium, 3=High):\n"))
    intensity = intensity_map.get(intensity_input, "Invalid")
    if intensity == "Invalid":
        print("Invalid intensity value.")
        return

    # Status mapping
    status_map = {1: "✅", 2: "❌", 3: "🟡"}
    status_input = int(input("Completed? (1=Yes, 2=No, 3=Partial):\n"))
    status = status_map.get(status_input, "Invalid")
    if status == "Invalid":
        print("Invalid status value.")
        return

    notes = input("Any notes?\n")

    data = {
        "timestamp": [now],
        "date": [date],
        "time": [time],
        "activity_type": [activity_type],
        "task": [task],
        "duration_min": [duration_min],
        "intensity": [intensity],
        "status": [status],
        "notes": [notes]
    }

    df = pd.read_csv("trak.csv") if os.path.exists("trak.csv") else pd.DataFrame(columns=data.keys())
    df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
    df.to_csv("trak.csv", index=False)

    print("✅ Entry added.")


#===================================================================================================================
def edit_entry():

    if not os.path.exists("trak.csv"):
        print("No data found.")
        return

    df = pd.read_csv("trak.csv")

    print("Here are the first 10 entries:\n")
    print(df.head(10))

    try:
        row_index = int(input("\nEnter row index to edit:\n"))
    except ValueError:
        print("❌ Invalid input. Must be a number.")
        return

    if row_index not in df.index:
        print("❌ Invalid index.")
        return

    field_map = {
        1: "activity_type",
        2: "task",
        3: "duration_min",
        4: "intensity",
        5: "status",
        6: "notes"
    }

    print("\nChoose what to edit:")
    for k, v in field_map.items():
        print(f"{k}. {v}")
    print("7. All fields")
    print("8. Cancel edit")

    try:
        choice = int(input("\nYour choice:\n"))
    except ValueError:
        print("❌ Invalid input.")
        return

    if choice in field_map:
        field = field_map[choice]
        new_value = input(f"Enter new value for {field}:\n")
        df.at[row_index, field] = new_value

    elif choice == 7:
        for field in field_map.values():
            new_value = input(f"Enter new value for {field}:\n")
            df.at[row_index, field] = new_value

    elif choice == 8:
        print("Edit canceled.")
        return
    else:
        print("❌ Invalid choice.")
        return

    df.to_csv("trak.csv", index=False)
    print("✅ Entry updated.")

#===================================================================================================================

def view_today_summary():
    if not os.path.exists("trak.csv"):
        print("No data found.")
        return

    df = pd.read_csv("trak.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    today = pd.Timestamp.now().date()
    today_df = df[df["timestamp"].dt.date == today]
    summary = today_df.groupby("activity_type")["duration_min"].sum()


    if today_df.empty:
        print("No entries for today.")
    else:
        print("Today's Entries:\n")
        print(today_df.tail(24))  # Or group by activity_type, etc.
        print("\nSummary (Time spent per activity type):")
        for activity, minutes in summary.items():
          print(f"🔸 {activity}: {int(minutes)} min")

        total = today_df["duration_min"].sum()
        print(f"\n🟩 Total time logged today: {int(total)} minutes")

     


#===================================================================================================================

def view_last_logs(n=5):
    if not os.path.exists("trak.csv"):
        print("No data found.")
        return

    df = pd.read_csv("trak.csv")
    print(f"Last {n} Logs:\n")
    print(df.tail(n))



