from flask import Flask, render_template, request, session
from cs50 import SQL
from datetime import date, timedelta

app = Flask(__name__)

db = SQL("sqlite:///data.db")

@app.route("/")
def default():
    return render_template("index.html", current_page='home')

@app.route("/member_data", methods=("GET", "POST"))
def memberData():
    if request.method == "GET":
        return render_template("memberdata.html", current_page="member_data")

@app.route("/cash_flow")
def cashFlow():
    return render_template("cashflow.html", current_page="cash_flow")

@app.route("/attendance", methods=("POST", "GET"))
def attendance():
    if request.method=="GET":
        return render_template("attendance.html", current_page="attendance")
    else:
        return dealWithSearches("attendance.html")

@app.route("/view_member_data", methods=("GET", "POST"))
def view_memb_data():
    if request.method == "GET":
        return render_template("viewmemberdata.html", current_page="view_member_data", recordqueries=False)
    else:
        return dealWithSearches("viewmemberdata.html")
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
        e_num = request.form.get("emergency_contact_number")
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
        pict = request.files["picture"]

        # Saving the picture locally
        pict.save(f"static/uploads/{pict.filename}")

        #Preliminary check to avoid inspect tampering is required

        today = current_date()

        duration = 30

        if memb_type == "Quarterly":
            duration = 90
        elif memb_type == "Half":
            duration = 182
        elif memb_type == "Yearly":
            duration = 365

        end_day = date_after_certain_days(date.today(), duration)
        
        # Inserting data into the persons table which generates a primary key
        db.execute("INSERT INTO persons(first_name, last_name, photo, gender, dob, temporary_address, permanent_address, mobile_number, emergency_number, married, blood_group, occupation) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", f_name, l_name, pict.filename, gender, dob, temp_addr, permanent_addr, m_num, e_num, marital_status, blood_grp, occupation)
        # Obtaining the data of the given person
        person_ids = db.execute("SELECT person_id FROM persons WHERE first_name LIKE ? AND last_name LIKE ? AND dob LIKE ? AND mobile_number = ? LIMIT 1", f_name, l_name, dob, m_num)
        # Returns a list of dictionaries which needs to be indexed properly
        person_id = person_ids[0]['person_id']
        # Inserting data into the members table for registration
        db.execute("INSERT INTO members(member_id, admission_date, household_head_first_name, household_head_last_name) VALUES (?, ?, ?, ?)", person_id, today, hh_f_name, hh_l_name)
        # Inserting data into memberships
        db.execute("INSERT INTO memberships(sport_category, current_plan, plan_start_date, plan_end_date, member_id) VALUES (?,?,?,?,?)", sprt_ctgry, memb_type, today, end_day, person_id)
        # print(f"{f_name}, {l_name}, {hh_f_name}, {hh_l_name}, {temp_addr}, {permanent_addr}, {m_num}, {e_num}, {gender}, {dob}, {sprt_ctgry}, {marital_status}, {occupation}, {blood_grp}, {memb_type}")
        return render_template("register.html")

@app.route("/fetch_data")
def fetch_data():
    id_in_url = request.args.get('member_id')
    details = db.execute("SELECT * FROM persons WHERE person_id = ?", id_in_url)[0]
    return render_template("fetch_data.html", current_page="member_data", details=details)

def current_date():
    return date.today().strftime("%Y-%m-%d")

def date_after_certain_days(todaysdate, dayCount):
    return todaysdate + timedelta(days=dayCount)

def dealWithSearches(redirecting_url):
            # This needs to be modified in order to join tables by taking id from the persons table but for now we just join for simplicity purposes
            f_name = request.form.get("m_first_name")
            l_name = request.form.get("m_last_name")
            records = list()
            if l_name:
                records = db.execute("SELECT * FROM persons WHERE perons.first_name LIKE ? and persons.last_name LIKE ?", f_name, l_name)
            else:
                records = db.execute("SELECT * FROM persons WHERE persons.first_name LIKE ?", f_name)
                return render_template(redirecting_url, recordqueries=True, records=records)