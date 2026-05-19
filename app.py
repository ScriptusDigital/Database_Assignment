import os   
from datetime import date, datetime, timedelta


from dotenv import load_dotenv
from flask_migrate import Migrate

from flask import (
    Flask,
    flash,
    redirect, 
    render_template,
    request,
    url_for
)
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user
)   

from forms import AssignmentForm, AssignmentStatusForm, RegistrationForm, LoginForm
from models import User, Expense, Assignment, TimetableEntry, db

load_dotenv()

app = Flask(__name__)

#====CONFIG====#

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   

#====CODE ADDED FOLLOWING NEON CONNECTION ISSUES====#
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
    "connect_args": {
            "connect_timeout":10
    }

}
           

#====DATABASE INIT====#

db.init_app(app)
migrate = Migrate(app, db)


#====LOGIN MANAGER====#
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id)) 

login_manager.login_view = 'login'
login_manager.login_message = (
    'Please log in to access StudentPilot.'
)

#====ROUTES====#

@app.route('/')
def home():
 return render_template('home.html')

#====DASHBOARD LOGIC====#

@app.route('/dashboard')
@login_required
def dashboard():
    today = date.today()
    next_week = today + timedelta(days=7)
   
    assignments = Assignment.query.filter_by(user_id=current_user.id).all()
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
   
    total_assignments = len(assignments)
    completed_assignments = sum(1 for item in assignments if item.status == "Completed")
    
    pending_assignments = total_assignments - completed_assignments 
    
    due_soon = (
        Assignment.query.filter(
            Assignment.user_id == current_user.id,
            Assignment.status != "Completed",
             Assignment.due_date >= today,
             Assignment.due_date <= next_week,
        )
        .order_by(Assignment.due_date.asc())
        .all()
    )

    overdue = (
        Assignment.query.filter(
            Assignment.user_id ==current_user.id,
            Assignment.status !="Completed",
             Assignment.due_date < today,
        )
        .order_by(Assignment.due_date.asc())
        .all()
    )

    total_spending = sum(expense.amount for expense in expenses)
    recent_expenses = (
        Expense.query.filter_by(user_id=current_user.id)
        .order_by(Expense.date.desc())
        .limit(5)
        .all()
        )
 
 #====DEFINITIONS FOR NEXT CLASS/EVENT LOGIC====#
    days_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    now = datetime.now()
    today_name = days_order[now.weekday()]
    current_time = now.time()

    today_next_class = (
        TimetableEntry.query    
        .filter(
            TimetableEntry.user_id == current_user.id,
            TimetableEntry.day_of_week == today_name,
            TimetableEntry.start_time >= current_time,
        )
    .order_by(TimetableEntry.start_time.asc())
    .first()
    )

    next_timetable_entry = today_next_class

    if not next_timetable_entry: 
        today_index = days_order.index(today_name)

        for offset in range(1, 8):
            next_day = days_order[(today_index + offset) % 7]

            next_timetable_entry = (
                TimetableEntry.query.filter_by(
                    user_id=current_user.id,
                    day_of_week=next_day,
                )
            .order_by(TimetableEntry.start_time.asc())
            .first() 
            )
        
            if next_timetable_entry:
              break
            
  #====Dashboard summary definitions====#
    return render_template('dashboard.html',
    total_assignments=total_assignments,
    completed_assignments=completed_assignments,
    pending_assignments=pending_assignments,
    due_soon=due_soon,
    overdue=overdue,
    total_spending=total_spending,
    recent_expenses=recent_expenses,
    next_timetable_entry=next_timetable_entry,
    )


 #====USER REGISTRATION====#

@app.route('/register', methods=['GET', 'POST'])
def register():
    form=RegistrationForm()

    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if form.validate_on_submit():
        username = form.username.data.strip()
        email = form.email.data.strip().lower()
        password = form.password.data

        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please log in.', 'warning')
            return redirect(url_for('login'))

    
        if User.query.filter_by(username=username).first():
            flash('Username already taken. Please choose a different one.', 'danger')
            return render_template('register.html', form=form)
    
        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()             

        flash('Registration successful! Please log in.', 'success')
    
        return redirect(url_for('login'))     
      
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        password = form.password.data
        remember = form.remember.data
  

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash(f'Welcome back, {user.username}.', 'success')
            return redirect(url_for('dashboard'))
     
        flash('Invalid email or password. Please try again.', 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

 #====BUDGET==#

@app.route('/budget', methods=['GET', 'POST'] )
@login_required
def budget():

  #====Expenses input and logic==#
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        category = request.form.get('category', '').strip()
        amount_text = request.form.get('amount', '').strip()
        date_text  = request.form.get('date', '').strip()
        notes = request.form.get('notes', '').strip()

        if not title or not category or not amount_text or not date_text:
            flash('Please fill out all required fields.', 'danger')
            return redirect(url_for('budget'))
        
        allowed_categories = [
            "Rent",
            "Food",
            "Transport",
            "Books",
            "Subscriptions",
            "Social",
            "Other",
        ]

        if category not in allowed_categories:
            flash('Please choose a valid category.','danger')
            return redirect(url_for('budget'))

        try:
            amount = float(amount_text)
        except ValueError:
            flash('Please enter a valid number for amount.', 'danger')
            return redirect(url_for('budget'))
        if amount <= 0:
            flash('Amount must be greater than zero.', 'danger')
            return redirect(url_for('budget'))
        try:
            expense_date = datetime.strptime(date_text, '%Y-%m-%d').date()
        except ValueError:
            flash('Please enter a valid date in YYYY-MM-DD format.', 'danger')
            return redirect(url_for('budget'))
        expense = Expense(
            title=title,
            category=category,
            amount=amount,
            date=expense_date,
            notes=notes,
            user_id=current_user.id
        )
        db.session.add(expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('budget'))

    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).all()
    total_spent = sum(expense.amount for expense in expenses)
    category_totals = {}
    for expense in expenses:
        category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.amount
            
    return render_template('budget.html', expenses=expenses, total_spent=total_spent, category_totals=category_totals)

#====Expense deletion logic - CRUD ==#
@app.route('/delete_expense/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.user_id != current_user.id:
        flash('You do not have permission to delete this expense.', 'danger')
        return redirect(url_for('budget'))
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted successfully.', 'success')
    return redirect(url_for('budget'))


#====Assignment input logic==#

@app.route('/assignments', methods=["GET", "POST"])
@login_required
def assignments():
    form = AssignmentForm()

    if form.validate_on_submit():
        assignment = Assignment(
        title=form.title.data.strip(),
        module_name=form.module_name.data.strip(),
        due_date=form.due_date.data,
        priority=form.priority.data,
        status=form.status.data,

        notes=form.notes.data.strip() if form.notes.data else "",
        user_id=current_user.id
        )
        
        db.session.add(assignment)
        db.session.commit()

        flash("Assignment added successfully.", "success")
        return redirect(url_for("assignments"))
       
    
    selected_status = request.args.get("status")
    allowed_statuses = ["Not started", "In progress", "Completed"]

    query = Assignment.query.filter_by(user_id=current_user.id)

    if selected_status in allowed_statuses:
        query = query.filter_by(status=selected_status)
    else:
        selected_status = None

    user_assignments = query.order_by(Assignment.due_date.asc()).all()

    status_forms = {}
    for assignment in user_assignments:
        status_form = AssignmentStatusForm()
        status_form.status.data = assignment.status
        status_forms[assignment.id] = status_form

    return render_template(
        "assignments.html",
    assignments=user_assignments,
    selected_status=selected_status,
    form=form,
    status_forms=status_forms,
    )


#====Update and delete function for assignment cards - CRUD FUNCTION==#
#===Based on elements of https://flask-sqlalchemy.readthedocs.io/en/stable/queries==#
#=== and https://bdavison.napier.ac.uk/web/flask/basics/crud==#
@app.route("/assignment/<int:assignment_id>/status", methods=["POST"])
@login_required
def update_assignment_status(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
   
    if assignment.user_id != current_user.id:
            flash("You don't have permission to update this assignment.", "danger")
            return redirect(url_for("assignments"))
    
    form = AssignmentStatusForm()

    if form.validate_on_submit():
        assignment.status = form.status.data
        db.session.commit()
        flash ("Assignment status updated.", "success")
    else:
        flash ("Please choose a valid status.", "danger")

    return redirect(url_for("assignments"))

@app.route("/assignment/<int:assignment_id>/delete", methods=["POST"])
@login_required
def delete_assignment(assignment_id):
        assignment = Assignment.query.get_or_404(assignment_id)

        if assignment.user_id != current_user.id:
            flash("You do not have permission to delete this assignment", "danger")
            return redirect(url_for("assignments"))
        
        db.session.delete(assignment)
        db.session.commit()

        flash("Assignment deleted.", "success")
        return redirect(url_for("assignments"))

#====Timetable route and logic==#
@app.route('/timetable', methods=['GET', 'POST'])
@login_required
def timetable():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    time_slots = ["08:00",
                  "09:00", 
                  "10:00", 
                  "11:00", 
                  "12:00", 
                  "13:00", 
                  "14:00",
                  "15:00" ,
                  "16:00",
                  "17:00"] 

    class_types = ["Lecture", "Tutorial", "Lab", "Seminar", "Study session", "Other"]


    if request.method =='POST':
        module_name = request.form.get("module_name", "").strip()
        class_type = request.form.get("class_type", "").strip()
        day_of_week = request.form.get("day_of_week", "").strip()
        start_time_text = request.form.get("start_time", "").strip()
        end_time_text = request.form.get("end_time", "").strip()
        location = request.form.get("location", "").strip()
        notes = request.form.get("notes", "").strip()


        if not module_name or not class_type or not day_of_week or not start_time_text or not end_time_text or not location:
            flash("Module name, class type, day, times and location are required.", "danger")
            return redirect(url_for("timetable"))
        
        if class_type not in class_types:
            flash("Please choose a valid class type.", "danger")
            return redirect(url_for("timetable"))
        
                
        if day_of_week not in days:
            flash("Please choose a valid weekday.", "danger")
            return redirect(url_for("timetable"))

        try:
            start_time = datetime.strptime(start_time_text, "%H:%M").time()
            end_time = datetime.strptime(end_time_text, "%H:%M").time()

        except ValueError:
                flash("Please enter valid times.", "danger")
                return redirect(url_for("timetable"))
        
        if end_time <= start_time:
                flash("End time must be after start time.", "danger")
                return redirect(url_for("timetable"))
        
        entry = TimetableEntry(
            module_name=module_name,
            class_type=class_type,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            location=location,
            notes=notes,
            user_id=current_user.id,
        )

        db.session.add(entry)
        db.session.commit()
        flash("Timetable entry added successfully.", "success")
        return redirect(url_for("timetable"))

    entries_by_day = {}
    for day in days:
            entries_by_day[day] = (
                TimetableEntry.query
                .filter_by(user_id=current_user.id, day_of_week=day)
                .order_by(TimetableEntry.start_time.asc())
                .all()

            )

    
    return render_template("timetable.html",
    days=days,
    time_slots=time_slots,
    entries_by_day=entries_by_day,
)


 #===User timetable delete logic===#
@app.route('/timetable/<int:entry_id>/delete', methods=['POST'])
@login_required
def delete_timetable_entry(entry_id):
    entry = TimetableEntry.query.get_or_404(entry_id)

    if entry.user_id != current_user.id:
        flash("You do not have permission to delete this timetable entry.", "danger")
        return redirect(url_for("timetable"))   

    db.session.delete(entry)
    db.session.commit()

    flash("Timetable entry deleted.", "success")
    return redirect(url_for("timetable"))



if __name__ == '__main__':
    app.run(debug=True, port=5005)        


    