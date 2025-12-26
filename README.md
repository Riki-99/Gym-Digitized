# Gym Digitized
#### Video Demo: <url>

## Description:
### Overview
This project was designed to solve a local problem I saw when visiting my local gym. When I went to my gym rather late at night, I saw one of the staff (accountant) calculating the net cashflow of that particular day by hand, on a sheet of paper which got me intrigued. I realized that a system was needed to digitize the records of the gym encompassing a lot of features regarding storing / editing the data of the staff and the members, dealing with the attendance and transactions, and showing the net cashflow. Here follows the description of all the features this project "Gym Digitized" encompasses.

### static
uploads: Used to store the uploads, which at the current time refers to the pictures uploaded during the registration of the staff and the members.

main.css: Despite bootstrap being used extensively for designing UI, this file has been used to customize the bootstrap templates with an attempt to make the site slightly more aesthetically pleasing.

### templates
This folder contains skeletons for all the webpages inside the website in html, each of explained below in alphabetical order:

#### attendance.html
 Searches for a member taking into account either first name or last name. The request is posted to "/attendance" which returns all the members matching the name (returns info on currently non active members as well). All the members having similar name spelling are listed in a table which shows mobile number and permanent address in addition to the member's name and id which helps to differentiate in cases of multiple members having the same first and last name. A button to "Mark Present" will appear for each record on the table i.e. for each member matching the name, which will send a JSON request to "/mark_present" which will internally work to mark the person present, adding the appropriate details in the attendance table. When clicked, the button will be disabled. After reloading, if "Mark Present" was clicked mistakenly, there is an option to "Undo Marking Present" which will send a JSON request to "/mark_absent". Also, to keep track of how long a member was in the gym, the "Mark leaving time" button needs to be pressed, which will send a request to "/mark_timeout" and the backend handles the rest. There is a button for "View Attendance in detail" which will be explored in "attendancedetails.html" description.


#### attendancedetails.html
Contains an interface where the user can set an initial date and a final date to get the attendance records from "/get_attendance_details". By default, the window is from 15 days ago to today. The response from backend is used to generate a table which displays all the members whose membership is active for at least one day in the given timeframe window.

#### editdata.html
Contains an interface to edit common data belonging to members and staff. The current values are set as the default values and changes can be made which will be submitted to the backend. In order to not change the data, the default values can be left as is without changing them and submitted.

#### editmemberdata.html
Extends 'editdata.html' to add member specific data and a submit button that submits to "/update_member_details" which updates the persons and members tables.

#### edit staffdata.html
Extends 'editdata.html' to add staff specific data and a submit button that submits to "/update_staff_details" which updates the persons and staff tables.

#### fetch_data.html
Shows the personal data of members from the persons and members tables and the membership history of the person. Also here lies the option to add a new membership (which does the job of renewal as well) by sending a renewal request to "/renew_membership".

#### financedetails.html
Contains an interface to select the starting and final dates (default set to 30 days ago - today) and gets records from the transactions table by sending a JSON request to "/get_financial_details". Displays the financial details for income as well as expense and hence shows the net cashflow over a certain period of time.

#### register.html
Contains an interface to register members as well as the staff. Using DOM manipulation, different staff / member specific fields will appear depending on the option selected for either "member" or "staff". The data can be submitted to the backend which will add the new details to the persons, members and memberships tables (if member option was selected) or persons and staff tables (if staff option was selected)

#### searchinginterface.html
Creates an interface to search data which can be re-used multiple times such as in "/attendance", "/view_member_data".

#### staffdetails.html
Shows the personal details of a particular staff, i.e. it's the staff counter part to              fetch_data.html

#### template.html
The basic and the foundational skeleton of the entire website which sets various features such as headers for confirmation / failed messages, the navigation bar and blocks which can be extended by other html documents vastly improving the code reusability aspect.

#### transactionreview.html
Creates a bill like table to review whether the details submitted from "/transactions" are correct. If correct the transaction is added to the transactions table and the data is discarded if rejected.

#### transactions.html
Contains an interface to add transaction records with all the details. There is a feature to add a new transaction category because all the contexts for a transaction cannot be possibly thought of beforehand. This submits the data to "transactionreview.html".

#### viewmemberdata.html
Shortlists all the members whose name matches the one searched through "/view_member_data" in a tabular format which can be clicked to get the details of a particular member among a list of multiple members sharing a common name.

#### viewstafflist.html
Lists all the staff in alphabetical order. There is no filtering by name for staff unlike members because of the practical implication that the gym which this project was modeled after contains very few staff members.

### app.py
The flask backend file which contains specifies the routes and deals with all the backend stuff. This file is the backbone of the logic implemented in this project.

### data.db
The sql database which stores all the tables mentioned up until this point and some tables which aren't mentioned but are necessary for the project.

### helpers.py
This file contains some helper functions and all the imports. Essentially everything apart from setting up routes is done in this file.

### sqlcode.sql
The sql code used to generate all the tables in the database.


