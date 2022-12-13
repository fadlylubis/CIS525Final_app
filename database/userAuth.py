from deta import Deta
from dotenv import load_dotenv
import os
from datetime import date

import streamlit_authenticator as stauth

utc_today = date.today()
today = utc_today.strftime("%m-%d-%Y")


load_dotenv()

KEY = os.getenv('KEY') 

deta = Deta('b0wokvr1_DWeHgiBtH1kYeakAJ3MnLaoagf2ndd4C')

db = deta.Base("users_db")


def insert_user(username, name, password):
    """Returns the user on a successful user creation, otherwise raises and error"""
    return db.put({"key": username, "name": name, "password": password})



def fetch_all_users():
    """Returns a dict of all users"""
    res = db.fetch()
    return res.items


def get_user(username):
    """If not found, the function will return None"""
    return db.get(username)


def update_user(username, updates):
    """If the item is updated, returns None. Otherwise, an exception is raised"""
    return db.update(updates, username)


def delete_user(username):
    """Always returns None, even if the key does not exist"""
    return db.delete(username)


