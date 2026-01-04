import json
import os

FILE_NAME = "progress.json"


def load_data():
    if not os.path.exists(FILE_NAME):
        return set()
    with open(FILE_NAME, "r") as f:
        return set(json.load(f))


def save_data(data):
    with open(FILE_NAME, "w") as f:
        json.dump(list(data), f)


def toggle_day(day):
    data = load_data()
    if day in data:
        data.remove(day)
    else:
        data.add(day)
    save_data(data)


def is_completed(day):
    data = load_data()
    return day in data


def get_completed_days():
    return len(load_data())
