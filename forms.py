from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, DecimalField,PasswordField, SelectField, StringField, SubmitField, TextAreaField, TimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length


#====Registration and login forms ==#

class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=2, max=150),
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Please enter an email address"),
            Email(message="Please enter a valid email email address"),
            Length(max=150),
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6),
        ]
    )

    confirm_password = PasswordField(
        "Confirm password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match.")
        ]
    )

    submit = SubmitField("Create account")


class LoginForm(FlaskForm):
    email = StringField(
        "Email", 
        validators=[

             DataRequired(message="Please enter your email address"),
            Email(message="Please enter an a valid email address"),
        ]
    )

    password = PasswordField(
        "Password", 
        validators=[
            DataRequired(),
        ]
    )

    remember = BooleanField("Remember me")
    submit = SubmitField("Log in")


#====Assigment input form fields ==#


class AssignmentForm(FlaskForm):
    title = StringField(
        "Assignment title",
        validators=[
            DataRequired(message="Please enter an assignment title."),
            Length(max=160, message="Assignment title must be 160 characters or fewer."),
        ]
    )

    module_name = StringField(
        "Module name",
        validators=[
            DataRequired(message="Please enter a module name."),
            Length(max=120, message="Module name must be 120 characters or fewer."),
        ]
    ) 

    due_date = DateField(
        "Due date",
        validators=[
            DataRequired(message="Please enter a due date."),
        ]
    ) 

    priority = SelectField(
        "Priority",
        choices=[
             ("", "Select priority"),
            ("Low", "Low"),
            ("Medium", "Medium"),
            ("High", "High"),
        ],
        default="Medium",
        validators=[
            DataRequired(message="Please choose a priority.")
        ]
    )

    status = SelectField(
        "Status",
       choices=[
            ("", "Select status"),
            ("Not started", "Not started"),
            ("In progress", "In progress"),
            ("Completed", "Completed"),
        ],
        default="Not started",
        validators=[
            DataRequired(message="Please choose a status.")
        ]
    )

    notes = TextAreaField("Notes")
    submit = SubmitField("Add assignment")


class AssignmentStatusForm(FlaskForm):
        status = SelectField(
        "Status",
       choices=[
            ("Not started", "Not started"),
            ("In progress", "In progress"),
            ("Completed", "Completed"),
        ],
        default="Not started",
        validators=[
            DataRequired(message="Please choose a status."),
        ]
    )

        submit = SubmitField("Update")
        

#====Expense form logic ==#

class ExpenseForm(FlaskForm):
    title = StringField(
          "Expense title",
          validators=[
                DataRequired(message="Please enter and expense title."),
                Length(max=200, message="Expense title must be 200 characters or fewer.")
          ]
    )               
     
    category = SelectField(
          "Category",
          choices=[
               ("", "Select a category"),
               ("Rent", "Rent"),
                ("Food", "Food"),
                 ("Transport", "Transport"),
                  ("Books", "Books"),
                   ("Subscriptions", "Subscriptions"),
                    ("Social", "Social"),
                     ("Other", "Other"),
          ],
        
        validators=[
                DataRequired(message="Please choose a category."),
        ]
    )

    amount = DecimalField(
          "Amount (€)",
          places=2,
          validators=[
                DataRequired(message="Please enter an amount."),
          ]
     )

    date = DateField(
        "Date",
        validators=[
                DataRequired(message="Please enter a date."),
          ]
    )

    notes = TextAreaField("Notes")

    submit = SubmitField("Add expense")

#====Timetable Form ==#

class TimetableEntryForm(FlaskForm):
    module_name = StringField(
          "Module_name",
          validators=[
                DataRequired(message="Please enter and module name."),
                Length(max=120, message="Module name must be 12o characters or fewer.")
          ]
    )      

       
    class_type = SelectField(
          "Class type",
          choices=[
               ("", "Select type"),
               ("Lecture", "Lecture"),
                ("Tutorial", "Tutorial"),
                 ("Lab", "Lab"),
                  ("Seminar", "Seminar"),
                   ("Study session", "Study session"),
                     ("Other", "Other"),
          ],
        
        validators=[
                DataRequired(message="Please choose a class type."),
        ]
    )

    day_of_week = SelectField(
          "Day",
          choices=[
               ("", "Select daay"),
               ("Monday", "Monday"),
                ("Tuesday", "Tuesday"),
                 ("Wednesday", "Wednesday"),
                  ("Thursday", "Thursday"),
                  ("Friday", "Friday"),
                     ("Saturday", "Saturday"),
                     ("Sunday", "Sunday"),
          ],
        
        validators=[
                DataRequired(message="Please choose a day."),
        ]
    )

    start_time = TimeField(
         "Start time",
         validators=[
              DataRequired(message="Please enter a start time.")
         ]
    )

    end_time = TimeField(
         "End time",
         validators=[
              DataRequired(message="Please enter an end time.")
         ]
    )

    location = StringField(
          "Location",
          validators=[
                DataRequired(message="Please enter a location."),
                Length(max=150, message="Location  must be 150 characters or fewer.")
          ]
    )      

    notes = TextAreaField("Notes")

    submit = SubmitField("Save entry")

               




        
