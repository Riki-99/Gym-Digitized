# All headers are included in helpers
from helpers import *

@app.route("/")
def default():
    return render_template("index.html", current_page='home')

@app.route("/member_data", methods=("GET", "POST"))
def memberData():
    if request.method == "GET":
        return render_template("memberdata.html", current_page="member_data")

@app.route("/cash_flow")
def cashFlow():
    transaction_categories = db.execute("SELECT * FROM transaction_type")
    return render_template("cashflow.html", current_page="cash_flow", transaction_categories=transaction_categories)

@app.route("/attendance", methods=("POST", "GET"))
def attendance():
    if request.method=="GET":
        return render_template("attendance.html", current_page="attendance", recordqueries=False)
    else:
        records = returnRecordsUsingNames()
        # Adding a new attribute to each record to know if a person is present that particular day
        for record in records:
            p_id = record["person_id"]
            datetoday=date.today().strftime("%Y-%m-%d")
            todaysrecord = db.execute("SELECT * FROM attendance WHERE person_id = ? AND todays_date = ?", p_id, datetoday)
            record["todaysrecord"] = todaysrecord
        return render_template("attendance.html", recordqueries=True, records=records)

@app.route("/mark_present", methods=["POST"])
def mark_present():
    data = request.get_json()
    member_id  = data["id"]
    todays_date = date.today().strftime("%Y-%m-%d")
    # Getting the hours for today's time
    timein_hours = datetime.now().hour
    # Getting the minutes for today's time
    timein_minutes = datetime.now().minute
    print(timein_hours, timein_minutes)
    # Preventing double addition to the table

    if not db.execute("SELECT * FROM attendance WHERE person_id = ? AND todays_date = ?", member_id, todays_date):
        db.execute("INSERT INTO attendance(person_id, todays_date, timein_hours, timein_minutes) VALUES (?,?,?,?)", member_id, todays_date, timein_hours, timein_minutes)
        return jsonify({"id": member_id, "date": todays_date, "timein_hours": timein_hours, "timein_minutes": timein_minutes})
    else:
        return jsonify({"message" : "Error already logged in for the day"})
    # Reponse sent in json format so that js can understand

# This is for unmarking any presenets that may have been accidentally marked
@app.route("/mark_absent", methods=["POST"])
def mark_absent():
    data = request.get_json()
    member_id  = data["id"]
    todays_date = date.today().strftime("%Y-%m-%d")
    db.execute("DELETE FROM attendance WHERE person_id = ? AND todays_date = ?", member_id, todays_date)
    # Reponse sent in json format so that js can understand
    return jsonify({"id": member_id, "date": todays_date})

@app.route("/mark_timeout", methods=["POST"])
def mark_timeout():
    data = request.get_json()
    member_id = data["id"]
    todays_date = date.today().strftime("%Y-%m-%d")
    timeout_hours = datetime.now().hour
    timeout_minutes = datetime.now().minute
    db.execute("UPDATE attendance SET timeout_hours = ? , timeout_minutes = ? WHERE  person_id = ? AND todays_date = ?", timeout_hours, timeout_minutes, member_id, todays_date)
    query = db.execute("SELECT * FROM attendance WHERE person_id = ? AND todays_date = ?", member_id, todays_date)
    return jsonify({"member_id" : member_id, "timeout_hours" : timeout_hours, "timeout_minutes" : timeout_minutes, "query" : query})

@app.route("/view_member_data", methods=("GET", "POST"))
def view_memb_data():
    if request.method == "GET":
        return render_template("viewmemberdata.html", current_page="view_member_data", recordqueries=False)
    else:
        records = returnRecordsUsingNames()
        return render_template("viewmemberdata.html", current_page="view_member_data", recordqueries=True)
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


@app.route("/new_transaction_category", methods=["POST"])
def new_transaction_category():
    data = request.get_json()
    name = data['name']
    direction = data['direction']
    db.execute("INSERT INTO transaction_type(name, direction) VALUES (?, ?)", name, direction)
    return jsonify({"Name" : name, "Direction" : direction})
            
if __name__ == "__main__":
    app.run(debug=True)