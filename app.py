# All headers are included in helpers
from helpers import *

@app.route("/")
def default():
    return render_template("index.html", current_page='home')

@app.route("/member_data", methods=("GET", "POST"))
def memberData():
    if request.method == "GET":
        return render_template("memberdata.html", current_page="member_data")

@app.route("/transactions")
def cashFlow():
    transaction_categories = db.execute("SELECT * FROM transaction_type")
    return render_template("transactions.html", current_page="transactions", transaction_categories=transaction_categories)

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
    
# For the attendance details interface
@app.route("/attendance_details")
def attendance_details():
    datetoday = date.today().strftime("%Y-%m-%d")
    date15daysago = (date.today() - timedelta(days=15)).strftime("%Y-%m-%d")
    return render_template("attendancedetails.html", datetoday=datetoday, date15daysago=date15daysago, current_page="attendance")

# Interface for doing json request response stuff
@app.route("/get_attendance_details", methods=["POST"])
def get_attendance_details():
    data = request.get_json()
    print(data["start_date"], data["end_date"])
    #Start date
    start = data["start_date"]
    #End date
    end = data["end_date"]
    #Time difference between start and end
    time_diff = (date.fromisoformat(end) - date.fromisoformat(start)).days
    #Array that contains all the dates for which attendance needs to be done
    days_array = []
    #Using MM-DD format for days, time_diff + 1 because we want to be inclusive of the end date specified
    for i in range(0, time_diff + 1):
        days_array.append(date_after_certain_days(date.fromisoformat(start), i).strftime("%m-%d"))
    active_members = db.execute("SELECT memberships.member_id, persons.first_name, persons.last_name FROM memberships FULL JOIN persons ON memberships.member_id = persons.person_id WHERE (memberships.plan_start_date <= ? AND memberships.plan_end_date >= ?) OR (memberships.plan_start_date <= ? AND memberships.plan_end_date >= ?)", end, end, start, start)
    for members in active_members:
        #Getting the days in an array when a particular member was present and adding it as a key in the members dictionary 
        present_days = db.execute("SELECT todays_date FROM attendance WHERE person_id = ? AND todays_date >= ? AND todays_date <= ?", members["member_id"], start, end)
        #Changing the YYYY-MM-DD format for the present_days to MM-DD format for easier access
        for day in present_days:
            day['todays_date'] = day['todays_date'][-5 :]
        members["present_days"] = present_days
    return jsonify({"active_members": active_members, "time_diff": time_diff, "days_array": days_array})


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
        return render_template("viewmemberdata.html", current_page="view_member_data", recordqueries=True, records=records)
@app.route("/data_analysis")
def data_analysis():
    return render_template("dataanalysis.html", current_page="data_analysis")

@app.route("/register", methods=("GET", "POST"))
def register():
    if(request.method == "GET"):
        return render_template("register.html", current_page="member_data", dateToday=date.today().strftime("%Y-%m-%d"))
    
    else:
        #Adding the data in here
        #Checking whether we're to be registering a member (0) or a staff (1)
        persons_class = request.form.get("persons_class")
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

        post = request.form.get("job_desc")

        salary = request.form.get('salary')

        start_day = request.form.get("plan_start_date")

        end_day = request.form.get("plan_end_date")

        print(pict.filename)
        # Saving the picture locally
        pict.save(f"./static/uploads/{pict.filename}")

        #Preliminary check to avoid inspect tampering is required

        today = current_date()

        if not start_day:
            start_day = today

        duration = 30

        if memb_type == "Quarterly":
            duration = 90
        elif memb_type == "Half":
            duration = 182
        elif memb_type == "Yearly":
            duration = 365
        if not end_day:
            end_day = date_after_certain_days(date.today(), duration)
        
        # Inserting data into the persons table which generates a primary key
        db.execute("INSERT INTO persons(first_name, last_name, photo, gender, dob, temporary_address, permanent_address, mobile_number, emergency_number, married, blood_group, occupation) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", f_name, l_name, pict.filename, gender, dob, temp_addr, permanent_addr, m_num, e_num, marital_status, blood_grp, occupation)
        # Obtaining the data of the given person
        person_ids = db.execute("SELECT person_id FROM persons WHERE first_name LIKE ? AND last_name LIKE ? AND dob LIKE ? AND mobile_number = ? LIMIT 1", f_name, l_name, dob, m_num)
        # Returns a list of dictionaries which needs to be indexed properly
        person_id = person_ids[0]['person_id']

        #For member
        if persons_class == 0 or persons_class == "0":
            # Inserting data into the members table for registration
            db.execute("INSERT INTO members(member_id, admission_date, household_head_first_name, household_head_last_name) VALUES (?, ?, ?, ?)", person_id, today, hh_f_name, hh_l_name)
            # Inserting data into memberships
            db.execute("INSERT INTO memberships(sport_category, current_plan, plan_start_date, plan_end_date, member_id) VALUES (?,?,?,?,?)", sprt_ctgry, memb_type, today, end_day, person_id)
            # print(f"{f_name}, {l_name}, {hh_f_name}, {hh_l_name}, {temp_addr}, {permanent_addr}, {m_num}, {e_num}, {gender}, {dob}, {sprt_ctgry}, {marital_status}, {occupation}, {blood_grp}, {memb_type}")
            return render_template("transactions.html", heading=f"Successfully registered new member : {f_name} {l_name} with ID :  <b style='font-size: 130%;'>{person_id}</b>!", )
        
        # For staff
        else:
             db.execute("INSERT INTO staff(joined_date, post, salary) VALUES (date('now'), ?, ?);", post, salary)
             return render_template("register.html", heading=f"Successfully registered new staff : {f_name} {l_name} with ID : {person_id}!")

@app.route("/fetch_data")
def fetch_data():
    id_in_url = request.args.get('member_id')
    details = db.execute("SELECT * FROM persons WHERE persons.person_id = ?", id_in_url)[0]
    ongoing_plans = db.execute("SELECT * FROM memberships WHERE member_id = ?", id_in_url)
    plan_ongoing = False
    if(len(ongoing_plans) != 0):
        plan_ongoing = True
    return render_template("fetch_data.html", current_page="member_data", details=details, plan_ongoing=plan_ongoing, ongoing_plans=ongoing_plans)

# Membership renewals may overlap if renewed before expiry / without setting appropriate date
@app.route("/renew_membership", methods=['POST'])
def renew_membership():
    data = request.get_json()
    print(data)
    id = data["id"]
    sport_category = data["sportCategory"]
    current_plan = data["currentPlan"]
    start = data["start"]
    end = data["end"]
    db.execute("INSERT INTO MEMBERSHIPS(sport_category, current_plan, plan_start_date, plan_end_date, member_id) VALUES (?, ?, ?, ?, ?)", sport_category, current_plan, start, end, id)
    membership_id = db.execute("SELECT membership_id FROM memberships WHERE member_id = ? AND sport_category = ? AND current_plan = ? AND plan_start_date = ? AND plan_end_date = ?", id, sport_category, current_plan, start, end)
    print(membership_id)
    return jsonify({"id": membership_id[0]["membership_id"], "start_date" : start, "end_date" : end, "sport_category" : sport_category, "current_plan" : current_plan})

@app.route("/new_transaction_category", methods=["POST"])
def new_transaction_category():
    data = request.get_json()
    name = data['name']
    direction = data['direction']
    db.execute("INSERT INTO transaction_type(name, direction) VALUES (?, ?)", name, direction)
    return jsonify({"Name" : name, "Direction" : direction})

@app.route("/transaction_review", methods=["POST"])
def transaction_details():
    direction = request.form.get("cash_flow_direction")
    amount = request.form.get("transaction_amount")
    category = request.form.get("transaction_category")
    category_description = db.execute("SELECT name FROM transaction_type WHERE id = ?", category)[0]["name"]
    second_party = request.form.get("second_party")
    person_id = request.form.get("person_id")
    print(f"Category : {category}")         
    if(not person_id):
        person_id = 0
    remarks = request.form.get("transaction_remarks")
    return render_template("transactionreview.html", direction=direction, amount=amount, category=category, second_party=second_party, person_id=person_id, remarks=remarks, current_page="transactions", category_description=category_description) 

@app.route("/confirm_transaction", methods=["POST"])
def confirm_transaction():
    data = request.get_json()
    # Direction for each category can be referred to using the transaction_type table in data.db
    direction = data["direction"]
    amount = data["amount"]
    category = data["transaction_category"]
    second_party = data["second_party"]
    person_id = data["person_id"]
    remarks = data["remarks"]
    # To check person validity
    personvalidity = True
    # For invalid person id
    status=f"Error: Person with id : {person_id} doesn't exist."
    success = False
    # If there is a person id, then we need to check whether the person actually exists
    if person_id:
        personvalidity = db.execute("SELECT * FROM persons WHERE person_id = ?", person_id)
    
    if personvalidity or person_id == 0:
        status = "Transaction Completed!"
        success = True
        
    if(personvalidity):
        db.execute("INSERT INTO transactions(amount, transaction_datetime, remarks, transaction_type_id, second_party_id, person_id) VALUES(?,datetime('now','localtime'),?,?,?,?);", amount, remarks, category, second_party, person_id)
    return jsonify({"amount" : amount, "remarks" : remarks, "category" : category, "second_party" : second_party, "person_id" : person_id, "success" : success,  "statusText" : status})

@app.route("/finance_details", methods=["GET"])
def finance_details():
    datetoday = date.today().strftime("%Y-%m-%d")
    date30daysago = (date.today() - timedelta(days=30)).strftime("%Y-%m-%d")
    return render_template("financedetails.html", current_page="finance_details", datetoday=datetoday, date30daysago=date30daysago)

@app.route("/get_financial_details", methods=["POST"])
def get_financial_details():
    data = request.get_json()
    start = f'{data["start_date"]} 00:00:00'
    end = f'{data["end_date"]} 00:00:00'
    # details = db.execute("SELECT * FROM transactions WHERE ")

    #Time difference between start and end
    time_diff = (date.fromisoformat(data["end_date"]) - date.fromisoformat(data["start_date"])).days
    #Array that contains all the dates for which financial details need to be displayed
    days_array = []
    #Using MM-DD format for days, time_diff + 1 because we want to be inclusive of one day before the specified end date
    for i in range(0, time_diff + 1):
        days_array.append(date_after_certain_days(date.fromisoformat(start), i).strftime("%m-%d"))
    records = db.execute("SELECT * FROM transactions WHERE transaction_datetime >= ? and transaction_datetime <= ?", start, end)
    return jsonify({"records": records, "time_diff": time_diff, "days_array": days_array})

if __name__ == "__main__":
    app.run(debug=True)