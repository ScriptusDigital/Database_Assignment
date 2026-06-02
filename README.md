# Project Title 

**StudentPilot**

## Project Description 

StudentPilot is a Flask-based student planning web application that helps users manage assigments, spending and weekly timetable entries in one place. The app allows users to create an account, lof in add coursework, deadlines, track assignment status, record xpenses, and build a weekly timetable from a personal dashboard. 

The project demonstates core Flack and database concepts such as routing, Jinja templating, user authentication, WTForm validation, PostgreSQL database integration, SQLAlchemy models, CRUD operations, flash messages and dynamic content rendering. It also features front-end techniques, including responsive layout, navigation toggling, assignment filtering, delete confirmations and a timetable modal window controlled with JavaScript. 

## Features 

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

#### Feature 6 - CRUD functionality
Assignments can be created, displayed, updated and deleted. Expenses and timetable entries can be created, displayed and deleted. User records can be created through registration and authenticated through login.

## Database 
The project uses PostgrSQL with Flask-SQLAlchemy. The main models are:
- `User`
- `Assignment`
- `Expense`
- `TimetableEntry`

Each assignment, expense and timetable entry is linked to a user through a foreign key. This means that each logged-in user only ever sees and manages their own data. 

### Database schema
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
The project was planned as a student dashboard app with three main areas: coursework, spending and timetable management. The aim was to build a practical Flask application that demonstrated user authentication, database backed CRUD functionality and dynamic page rendering. The core routes were planned around the main user journey: Home>registration>login>dashboard>assignments>budget>timtetabl. The database was therefore designed around a central 'user' model connected to the assignment, expnse and timetable records. This allowed each user's data to be filtered by `current_user.id`. 

### Form handling, WTForms and Flask-Migrate
The application was orignally designed around manual form handling while the core functionality was being built. This helped keep the early version focussed on getting routes, templates, database models and CRUD operations working. 

Once the core site was stable and time allowed, I improved the structure by migrating the forms to WTForms and Flask-WTF. This moved validation into `forms.py`, made the route logic cleaner and added and extra layer of protection (CSRF). 

Flask-Migrate was also added after the database models were stable. This allowed the database schema to be managed through migrations rather than relying on a simple table creation workflow, making the project easier for me to manage in terms of build workflow as the application grew.  

### Front-end and interactivity
Jinja templates were used to render the pages while keeping a shared structure through `base.html` CSS was kept in a separate style sheet. I chose to write the CSS manually rather than use Bootstrap because I wanted more control over the layout, spacing, colours, and visual identity of the app. 

Javascript is used for the mobile navigation toggle, delete confirmation warnings, assignment status filtering, timetable modal opening and closing, ad timetable slot pre-filling. The timetable modal uses data attributes from the clicked calendar slot to populate the day, start time and end time fields. 


## Challenges Faced

### Connect routes, templates and forms
On of the main challengs was keeping the Flask routes, WTForms field names and Jinja template references aligned. Small naming differences and typos caused a lot errors, especially during the the mirgration from manual form handling to WTForms. 

### Migrating after the core build

The app was already working before the migration to WTForms and Flask-Migrate. Refactoring a stable app meant a lot of back and forth between pages and errors. I completed the migration page bu page so that each area could be tested before moving on. 

If I were starting the project again, I would introduce WTForms and Flask-Migrate earlier. However, beginning with more direct-handling was useful because it helped me understand the underlying Flask logic around POST requests, validation and database commits. Refactorying to WTForms later made the benefits clearer, particularly around cleaner route logic, centralised validation and protection. 

### Timetable modal

The timetable page was the most complex job on the project as it combines database records, a calendar grid, a modal form and Javascript pre-filling. When the timetable form was migrated to WTForms, the form fields had to keep the same IDs used by the JavaScript. 

## Testing 

Manual testing was carried out throughout development. The main areas tested were:
- user registration, duplicate account checks, login and logout
- protected route behaviour for unauthenticated users
- adding, displaying, updating, filtering and deleteing assignments, expenses and classes in the timetable
- total spending and category summary calculations
- timetable modal opening, closing, and slot pre-filling
- dashboard summaries including due-soon assigment, overdue assignments, recent expenses and next class
- JavaScript behaviour including navigation toggle, delete confirmation and assignment filtering
- validation behaviour for required fileds, email format, password confirmation and invalid timetable times. 

## Usage

### For Anonymous Users
- View the homepage 
- Register an account
- Login to access the app
- Be redirected to the login page when trying to access protected pages

### For Logged-In Users
- **Dashboard**: View assignment totals,spending totals, recent expenses, due-sson assignments, overdue assignments and next class
- **Assignments**: Add coursework, set due dates, choose priority, track progress and delete assignemnts
- **Assignment status updates**: Update assignment progress as Not started, In progress or Completed
- **Budget**: Add expenses, view total spending, view spending by category and delete expense records
- **Timetable**: Add weekly class entries using the calendar modal and delete timtable entries
- **Logour**: End the current user session

### Routes Overview

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Homepage |
| `/register` | GET, POST | User registration |
| `/login` | GET, POST | User login |
| `/logout` | GET | User logout |
| `/dashboard` | GET | User dashboard summary |
| `/assignments` | GET, POST | view and add assignemnts |
| `/assignment/<assignment_id>/status`| POST | Update assignment status |
| `/assignment/<assignment_id>/delete` | POST | Delete assignment |
| `/budget` | GET, POST | view budget page and add expenses |
| `/delete_expense/<expense_id>` | POST | Delete expense |
| `/timetable` | GET, POST | view timetable and add timetable entried |
| `/timetable/<entry_id>/delete` | POST | Delete timetable entry |


## External Resources Used

### CRUD and database queries

The assignment update and delete functionality was based on elements from Flask-SQLAlchemy query documentaion and a FLASK CRUD example

- [Flask-SQLAlchemy - Queries](https://flask-sqlalchemy.readthedocs.io/en/stable/queries)

- [Brian Davison - Flask CRUD examples](https://bdavison.napier.ac.uk/web/flask/basics/crud)

### Assignment filtering
The JavaScript assigment status filter was based on examples:

- [GeeksforGeeks - How to create a filter list using JavaScript](https://www.geeksforgeeks.org/javascript/how-to-create-a-filter-list-using-javascript/)

- [CSS-Tricks - In-page filtered search with vanilla JavaScript](https://css-tricks.com/in-page-filtered-search-with-vanilla-javascript)


### Timetable modal and calendar interaction
The timetable calendar and modal pre-fill behaviour were adapted from time-block calendar tutorials and examples:

- [Codyyn - Time Block Calendar](https://codynn.com/labs/create/time-block-calendar)

- [Youtube timetable/calendar tutorial](https://www.youtube.com/watch?v=jJZRIOOw6zI)

### CSS Variables
CSS custom properties used to make the stylesheet easier to manage and keep colours, spacing and shared values consistent:

- [W3Schools - CSS Variables](https://www.w3schools.com/css/css3_variables.asp)

### Images and media
- ‘favicon.jpg’ generated in ChatGPT

## Development Notes
### Flask functionality used
The project makes use of: 
- Flask routes
- Jinja templating
- GET and POST request handling
- redirect and url_for
- flash messaging
- dynamic content rendering
- Flask-Login authentication
- Flask-SQLAlchemy models
- PostgreSQL database storage 
- Flask-Migrate database migrations
- WTForms validation
- CRUD operations
- environmentsal variables
 

## Deployed site
This project is available at: 
[GitHub Repository](https://github.com/ScriptusDigital/Database_Assignment)

## Deployment on Render
This project is deployed on Render using the linked GitHub repository. The application reads config values such as `SECRET_KEY` and `DATABASE_URL`
from environment variables, which can be set through the Render dashboard. The live deployed version is available through the link below. 

## Live deployment site
The application is available at: 
[Live App](https://database-assignment-vfqa.onrender.com)

