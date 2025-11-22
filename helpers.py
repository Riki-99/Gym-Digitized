from flask import Flask, render_template, request, session, jsonify
from cs50 import SQL
from datetime import date, timedelta, datetime

app = Flask(__name__)

db = SQL("sqlite:///data.db")

def current_date():
    return date.today().strftime("%Y-%m-%d")

def date_after_certain_days(todaysdate, dayCount):
    return todaysdate + timedelta(days=dayCount)

def returnRecordsUsingNames(f_name=None, l_name=None):
            # This needs to be modified in order to join tables by taking id from the persons table but for now we just join for simplicity purposes
            if(f_name is None):
                f_name = request.form.get("m_first_name")
            if(l_name is None):
                l_name = request.form.get("m_last_name")
            records = list()
            if l_name:
                records = db.execute("SELECT * FROM persons WHERE persons.first_name LIKE ? and persons.last_name LIKE ? ORDER BY persons.first_name", f_name, l_name)
            else:
                records = db.execute("SELECT * FROM persons WHERE persons.first_name LIKE ? ORDER BY persons.first_name", f_name)
            return records

      