import json, os
from datetime import timedelta


def file(user):
    return f"progress_{user}.json"


def load_progress(user):
    if not os.path.exists(file(user)):
        return set()
    with open(file(user)) as f:
        return set(json.load(f))


def save_progress(user, data):
    with open(file(user), "w") as f:
        json.dump(list(data), f)


def toggle_day(user, day):
    data = load_progress(user)
    data.remove(day) if day in data else data.add(day)
    save_progress(user, data)


def is_completed(user, day):
    return day in load_progress(user)


def completed_count(user):
    return len(load_progress(user))


def get_streaks(user, df):
    completed = sorted(load_progress(user))
    if not completed:
        return 0, 0

    dates = [df.loc[df.Day == d, "Date"].values[0] for d in completed]
    dates.sort()

    longest = current = streak = 1
    for i in range(1, len(dates)):
        if dates[i] - dates[i - 1] == timedelta(days=1):
            streak += 1
            longest = max(longest, streak)
        else:
            streak = 1

    today = df.Date.max()
    current = 0
    for d in reversed(dates):
        if today - timedelta(days=current) == d:
            current += 1
        else:
            break

    return current, longest
