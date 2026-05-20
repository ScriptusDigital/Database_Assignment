from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, DecimalField,PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length


#====Registration and login ==#

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
            DataRequired(),
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
            DataRequired(),
       
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


    #====Assignment forms ==#


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
        

      #====Expense forms logic ==#

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


               




        
