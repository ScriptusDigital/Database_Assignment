# Project Title 

**Student Pilot**



## Project Description 

StudentPilot is a Flask-based student planning web application that helps users manage assigments, spending and weekly timetable entries in one place. The app allows users to create an account, lof in add coursework, deadlines, track assignment status, record xpenses, and build a weekly timetable from a personal dashboard. 

The project demonstates core Flack and database concepts such as routing, Jinja templating, user authentication, WTFOrm calidation, PostreSQL database integration, SQLAlchemy models, CRUD operations, flash messages and dynamic content rendering. It also features front-end techniques, including responsive layout, navgaion toggling, assignment filtering, delete confirmations and a timetable modal window controlled with JavaScript. 

##Features 

#### Feature 1 - User registration and login 
Users can register with a username, email address and password. Passwords are hashed before being stored in the database. Users can then log in and log out using Flask-Login. Protected routes then ensure that only logged-in users can access the dashboard, assigments, budget and timetable pages. 

#### Feature 2 - Personal dashboard
The dashboard gives users a quick summary of their student information. It displays total assignments, completed assignments, pending assignments, total spending, next class, recent expenses, assignments due soon and ocerdue assigments. The dashboard uses database queries filtered by the logged-in user so that they can only access their own records. 


#### Feature 3 - Assignment tracking 
Users can add assigments with a title, module nam, due date, priority, status and optional notes. Assignments can be updated by changing their status to Not started, In progress or Completed. The assignment page also includes a JavaScript filter so users can view assignments by status. 

#### Feature 4 - Budget tracking 
Users can add expenses with a title, category, amount, date and optional notes. Th budhet page displays total spending, number of expense records, number of categories used, spending by category and a full expense history. Useres can also delete expense records. 

#### Feature 5 - Weekly timetable 
Users can create a weekly timetable by clicking on emppty calendar slots. A modal form opens and automatically fills in the selected day, start time and end time. Users can then add the module name, class type, location and notes. Timetable entries are shown in the correct day and time slot and can be deleted.  

#### Feature 5 - CRUD functionality
The project includes CRUD functionlaity accross the main parts of the app. Assignments, expenses and timetable entries can be created, displayed, updated and deleted. User records can be created with registration and authenticated through logic. 

## Database 
The project uses PostgrSQL with Flask-SQLAlchemy. The main models are:
- 'User'
- 'Assignment'
- 'Expense
- 'TimetableEntry

Each assignment, expense and timetable entry is linked to a user through a foreign key. This means that each logged-in user only ever sees and manages their own data. 

###
![Database schema](static/images/Database_Schema.png)

## Design choices