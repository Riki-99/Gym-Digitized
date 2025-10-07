from flask import Flask, render_template, request, session
from cs50 import SQL
from datetime import date, timedelta

app = Flask(__name__)

db = SQL("sqlite:///data.db")

@app.route("/")
def default():
    return render_template("index.html", current_page='home')

@app.route("/member_data")
def memberData():
    return render_template("memberdata.html", current_page="member_data")

@app.route("/cash_flow")
def cashFlow():
    return render_template("cashflow.html", current_page="cash_flow")

@app.route("/attendance")
def attendance():
    return render_template("attendance.html", current_page="attendance")

@app.route("/view_member_data")
def view_memb_data():
    return render_template("viewmemberdata.html", current_page="view_member_data")

@app.route("/data_analysis")
def data_analysis():
    return render_template("dataanalysis.html", current_page="data_analysis")

@app.route("/register", methods=("GET", "POST"))
def register():
    if(request.method == "GET"):
        return render_template("register.html", current_page="member_data")
    
    else:
        #Adding the data in here
        #First name
        f_name = request.form.get("m_first_name")
        #Last name
        l_name = request.form.get("m_last_name")
        #Household head first name
        hh_f_name = request.form.get("house_head_first_name")
        #Household head last Name
        hh_l_name = request.form.get("house_head_last_name")
        #Temporary address
        temp_addr = request.form.get("temporary_address")
        #Permanent address
        permanent_addr = request.form.get("permanent_address")
        #Mobile number
        m_num = request.form.get("mobile_number")
        #Emergency number
        e_num = request.form.get("emergency_number")
        #Gender
        gender= request.form.get("gender")
        #DOB
        dob = request.form.get("dob")
        #Sport category
        sprt_ctgry = request.form.get("sport_category")
        #Marital status
        marital_status = request.form.get("marital_status")
        #Occupation
        occupation = request.form.get("occupation")
        #Blood group
        blood_grp = request.form.get("blood_group")
        #Membership type
        memb_type = request.form.get("membership_type")
        #Picture
        pict = request.form.get("picture")

        #Preliminary check to avoid inspect tampering is required

        today = current_date()

        duration = 30

        if memb_type == "Quarterly":
            duration = 90
        elif memb_type == "Half":
            duration = 182
        elif memb_type == "Yearly":
            duration = 365

        end_day = date_after_certain_days(today, duration)
        
        # Inserting data into the persons table which generates a primary key
        db.execute("INSERT INTO persons(first_name, last_name, photo, gender, dob) VALUES (?, ?, ?, ? , ?)", f_name, l_name, pict, gender, dob)
        # Obtaining the data of the given person
        person_id = db.execute("SELECT person_id FROM persons WHERE first_name LIKE ? AND last_name LIKE ? AND dob LIKE ? AND photo = ? COUNT 1", f_name, l_name, dob, pict)
        # Inserting data into the members table for registration
        db.execute("INSERT INTO members(member_id, admission_date, sport_category, current_plan, plan_start_date, plan_end_date, household_head_first_name, household_head_last_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", person_id, today, sprt_ctgry, memb_type, today, end_day, hh_f_name, hh_l_name)

        # print(f"{f_name}, {l_name}, {hh_f_name}, {hh_l_name}, {temp_addr}, {permanent_addr}, {m_num}, {e_num}, {gender}, {dob}, {sprt_ctgry}, {marital_status}, {occupation}, {blood_grp}, {memb_type}")
        return render_template("register.html")

def current_date():
    return date.today().strftime("%Y-%m-%d")

def date_after_certain_days(todaysdate, dayCount):
    return todaysdate + timedelta(days=dayCount)