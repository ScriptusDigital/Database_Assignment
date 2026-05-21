# Project Title 

**Student Pilot**



## Project Description 

StudentPilot is a Flask-based student planning web application that helps users manage assigments, spending and weekly timetable entries in one place. The app allows users to create an account, lof in add coursework, deadlines, track assignment status, record xpenses, and build a weekly timetable from a personal dashboard. 

The project demonstates core Flack and database concepts such as routing, Jinja templating, user authentication, WTFOrm calidation, PostreSQL database integration, SQLAlchemy models, CRUD operations, flash messages and dynamic content rendering. It also features front-end techniques, including responsive layout, navgaion toggling, assignment filtering, delete confirmations and a timetable modal window controlled with JavaScript. 

##Features 

#### Feature 1 - User registration and login 
Users can register with a username, email address and password. Passwords are hashed before being stored in the database. Users can then log in and log out using Flask-Login. Protected routes then ensure that only logged-in users can access the dashboard, assignments, budget and timetable pages. 

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

### Theme a visual style
The visual style was designed as a clean studen productivity platform. The idea was to make the application feel and appear practical, organised and easy to use rather than overly decorative. The interface uses cards, panels, rounded corners, clear headings and a neutral palette. 

### layout
The main pages use repeated layout patterns so that the application feels consistent. These includ stat cards, record cards, form panels, two-column sextions and stacked dashboard panels. The timetable page uses a grid layout to present a weekly calendar. 

### Colours
The colour palette uses soft background tones, white panels and darker text elements for contract. The intention was to keep the interface readable and calm while giving the buttons and interactive elements visual emphasis. 

#### Responsiveness
The layout was designed to adapt to different screen sizes. Wider screens use two-column layouts, while smaller screens stack the content vertically. The timetable uses horizontal scrolling where required to preserve the grid structure. 

## Development Process

### Project Planning
The project was planned as a student dashboard app with three main areas: coursework, spending and timetable management. The aim was to build a practical Flask application that demonstrated user authentication, database backed CRUD functionality and dynamic page rendering. The core routes were planned around the main user journey: Home>registration>login>dashboard>assignments>budget>timtetabl. The database was therefore designed around a central 'user' model connected to the assignment, expnse and timetable records. This allowed each user's data to be filtered by 'current_user.id'. 

### Form handling, WTForms and Flask-Migrate
The application was orignally designed around manual form handling while the core functionality was being built. This helped keep the early version focussed on getting routes, templates, database models and CRUD operations working. 

Once the core site was stable and time allowed, I improved the structure by migrating the forms to WTForms and Flask-WTF. This moved validation into 'forms.py', made the route logic cleaner and added and extra layer of protection (CSRF). 

Flask-Migrate was also added after the database models were stable. This allowed the database schema to be managed through migrations rather than relying on a simple table creation workflow, making the project easier for me to manage in terms of build workflow as the application grew.  

### Front-end and interactivity
Jinja templates were used to render the pages while keeping a shared structure through 'base.html'CSS was kept in a separate style sheet. I chose to write the CSS manually rather than use Bootstrap because I wanted more control over the layout, spacing, colours, and visual identity of the app. 

Javascript is used for the mobile navigation toggle, delete confirmation warnings, assignment status filtering, timetable modal opening and closing, ad timetable slot pre-filling. The timetable modal uses data attributes from the clicked calendar slot to populate the day, start time and end time fields. 


##Challenges Faced