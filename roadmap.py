from datetime import date, timedelta
import calendar

def generate_roadmap():
    topics = [
        "Python Basics", "Data Types", "Operators", "Strings",
        "Lists", "Dictionaries", "Conditionals", "Loops",
        "Functions", "Practice", "Mini Project"
    ]

    roadmap = []
    start = date.today()

    for day in range(1, 366):
        current_date = start + timedelta(days=day - 1)

        roadmap.append({
            "day": day,
            "date": current_date,
            "month": calendar.month_name[current_date.month],
            "topic": topics[(day - 1) % len(topics)],
            "xp": 10
        })

    return roadmap
