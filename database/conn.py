from deta import Deta
from dotenv import load_dotenv
import os
from datetime import date


utc_today = date.today()
today = utc_today.strftime("%m-%d-%Y")


load_dotenv()

KEY = os.getenv('KEY') 

deta = Deta(KEY)

db = deta.Base("main_db")


def insert_data(time_of_day, meal,calories, notes, name):
    return db.insert({
        "Day": today,
        "TimeOfDay": time_of_day,
        "Meal": meal,
        "Calories":calories,
        "Notes": notes,
        "Name": name
    })

def get_all_data():
    """Returns a dict of all users"""
    res = db.fetch()
    return res.items

