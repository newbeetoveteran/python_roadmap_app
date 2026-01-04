from datetime import date, timedelta

start_date = date(2026, 1, 4)

topics_cycle = [
    ("Python Basics", "Syntax, variables"),
    ("Data Types", "Numbers, strings"),
    ("Operators", "Arithmetic, logic"),
    ("Strings", "Methods"),
    ("Lists", "Operations"),
    ("Dictionaries", "Key-value"),
    ("Conditionals", "if/else"),
    ("Loops", "for/while"),
    ("Functions", "def/return"),
    ("Practice", "Problem solving"),
    ("Mini Project", "Small app"),
]

rows = []

for day in range(1, 366):
    week = f"Week {((day - 1) // 7) + 1}"
    d = start_date + timedelta(days=day - 1)
    topic, practice = topics_cycle[(day - 1) % len(topics_cycle)]
    rows.append((week, day, d.isoformat(), topic, practice))

with open("roadmap_data.py", "w", encoding="utf-8") as f:
    f.write("import pandas as pd\n\n")
    f.write("DATA = [\n")
    for r in rows:
        f.write(f"    {r},\n")
    f.write("]\n\n")
    f.write("""
def load_roadmap():
    df = pd.DataFrame(DATA, columns=["Week", "Day", "Date", "Topic", "Practice"])
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.strftime("%B")
    return df
""")

print("✅ roadmap_data.py created successfully!")
