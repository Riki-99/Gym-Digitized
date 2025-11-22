CREATE TABLE persons(
    person_id INTEGER, /*primary key for  member*/
    first_name TEXT,
    last_name TEXT,
    photo TEXT, /* passport size photo name, which will be stored in /static/uploads */
    gender VARCHAR(1),/* M or F or O (Male, Female, Other) */
    dob DATE,
    temporary_address TEXT,
    permanent_address TEXT,
    mobile_number TEXT,
    occupation TEXT,
    emergency_number TEXT,
    married INTEGER, /* 0 for unmarried 1 for married*/
    blood_group TEXT,
    PRIMARY KEY (person_id) /* Automatically increments the id for new record in the table */
);

CREATE TABLE members(
    member_id INTEGER,
    admission_date DATE,
    household_head_first_name TEXT,
    household_head_last_name TEXT,
    FOREIGN KEY (member_id) REFERENCES persons(person_id)
    PRIMARY KEY(member_id)
);

CREATE TABLE memberships(
    membership_id INTEGER,
    sport_category TEXT,
    current_plan TEXT,
    plan_start_date DATE,
    plan_end_date DATE,
    member_id INTEGER,
    FOREIGN KEY (member_id) REFERENCES members(member_id)
    PRIMARY KEY(membership_id)
);

CREATE TABLE staff(
    staff_id INTEGER,
    joined_date DATE,
    salary NUMBER,
    post TEXT,
    FOREIGN KEY (staff_id) REFERENCES persons(person_id)
    PRIMARY KEY(staff_id)
);

CREATE TABLE transaction_type(
    id INTEGER,
    name TEXT,
    direction INT, /* 1 Income/ 0 Expenditure */
    PRIMARY KEY(id)
);

CREATE TABLE transaction_second_party(
    id INT,
    type TEXT, /*Other party type : member, staff, external*/
    PRIMARY KEY (id)
    );

CREATE TABLE transactions(
    transaction_id INT,
    amount NUMBER,
    transaction_date DATE,
    remarks TEXT, /* For externals, the name should be written in remarks*/
    transaction_type_id INT, 
    second_party_id INT, /* Other party maybe a MEMBER, STAFF, EXTERNAL */
    person_id INT, /* If id is applicable, members only for now but hopefully staff too somewhat later*/
    PRIMARY KEY (transaction_id),
    FOREIGN KEY (person_id) REFERENCES persons(person_id),
    FOREIGN KEY (second_party_id) REFERENCES transaction_second_party(id),
    FOREIGN KEY (transaction_type_id) REFERENCES transaction_type(id)
);

CREATE TABLE attendance(
    person_id INTEGER,
    todays_date DATE,
    timein_hours NUMBER, /* 24 hour format */
    timein_minutes NUMBER,
    timeout_hours NUMBER,
    timeout_minutes NUMBER,
    PRIMARY KEY(person_id, todays_date)
    FOREIGN KEY(person_id) REFERENCES members(member_id)
);

