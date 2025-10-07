CREATE TABLE persons(
    person_id INTEGER, /*primary key for  member*/
    first_name TEXT,
    last_name TEXT,
    photo BLOB, /* passport size photo */
    gender VARCHAR(1),/* M or F or O (Male, Female, Other) */
    dob DATE,
    PRIMARY KEY (person_id) /* Automatically increments the id for new record in the table */
);

CREATE TABLE members(
    member_id INTEGER,
    admission_date DATE,
    sport_category TEXT,
    current_plan TEXT, /* Gym, Zumba etc*/
    plan_start_date DATE,
    plan_end_date DATE,
    household_head_first_name TEXT,
    household_head_last_name TEXT,
    FOREIGN KEY (member_id) REFERENCES persons(person_id)
);

CREATE TABLE staff(
    staff_id INTEGER,
    joined_date DATE,
    salary NUMBER,
    post TEXT,
    FOREIGN KEY (staff_id) REFERENCES persons(person_id)
);

CREATE TABLE transactions(
    transaction_id INT,
    purpose TEXT,
    amount NUMBER,
    transaction_date DATE,
    remarks TEXT, /* For externals, the name should be written in remarks*/
    transaction_type TEXT, /* Income/Expenditure */
    other_party_type TEXT, /* Other party maybe a MEMBER, STAFF, EXTERNAL */
    person_id INT, /* If id is applicable, members only for now but hopefully staff too somewhat later*/
    PRIMARY KEY (transaction_id),
    FOREIGN KEY (person_id) REFERENCES persons(person_id)
);

CREATE TABLE attendance(
    person_id INTEGER,
    todays_date DATE,
    present NUMBER,
    timein_hours NUMBER, /* 24 hour format */
    timein_minutes NUMBER,
    timeout_hours NUMBER,
    timeout_seconds NUMBER,
    PRIMARY KEY(person_id, todays_date)
    FOREIGN KEY(person_id) REFERENCES persons(person_id)
);