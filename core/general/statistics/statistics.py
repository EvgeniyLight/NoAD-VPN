from constants.constants import PLUS_ONE, LAST_RUN_FILE
import requests, os
from datetime import datetime, date

def user_visited_day():
    try:
        current_day = datetime.now().day
        payload = {
            "day_of_month": current_day 
        }
        requests.post(PLUS_ONE, json=payload)
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def run_once_per_day():
    today = date.today()

    if os.path.exists(LAST_RUN_FILE): 
        with open(LAST_RUN_FILE, "r") as file: 
            last_run_date = date.fromisoformat(file.read().strip())
        if last_run_date == today:
            return
    user_visited_day()

    with open(LAST_RUN_FILE, "w") as file:
        file.write(today.isoformat())
