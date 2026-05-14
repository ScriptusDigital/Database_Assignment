
import datetime
import os   

from dotenv import load_dotenv


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
from models import User, Expense, Assignment, db

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
           

#====DATABSE INIT====#

db.init_app(app)
with app.app_context():
    db.create_all()


#====LOGIN MANAGER====#
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))     

login_manager.login_view = 'login'
login_manager.login_message = (
    'Please log in to access your StudentPilot dashboard.'
)

#====ROUTES====#

@app.route('/')
def home():
 return render_template('home.html')



@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
 
 #====USER REGISTRATION====#

@app.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        flash('You are already registered.', 'info')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password') 
        confirm_password = request.form.get('confirm_password')
        
        if not username or not email or not password:
         flash('Please fill out all fields.', 'danger')
         return render_template('register.html')
    
        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return render_template('register.html')
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('register.html')

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
         flash('Email already registered. Please log in.', 'warning')
         return redirect(url_for('login'))
    
        if User.query.filter_by(username=username).first():
            flash('Username already taken. Please choose a different one.', 'danger')
            return render_template('register.html')
    
        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()             

        flash('Registration successful! Please log in.', 'success')
    
        return redirect(url_for('login'))     
      
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get("remember") == "on"
  

        user = User.query.filter_by(email=email).first()

        print(f"USER: {user}")  # Debugging line

        if user:
            print(f"PASSWORD CHECK: {len(user.password_hash)}")  # Debugging line
       
            print(f"HASH LENGTH: {len(user.password_hash)  }")  # Debugging line
        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash(f'Welcome back, {user.username}', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('login.html')


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

  #====Expenses input andlogic==#
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        amount_text = request.form.get('amount')
        date_text  = request.form.get('date')
        notes = request.form.get('notes')

        if not title or not category or not amount_text or not date_text:
            flash('Please fill out all required fields.', 'danger')
            return render_template('budget.html')
        try:
            amount = float(amount_text)
        except ValueError:
            flash('Please enter a valid number for amount.', 'danger')
            return render_template('budget.html')
        if amount <= 0:
            flash('Amount must be greater than zero.', 'danger')
            return render_template('budget.html')
        try:
            expense_date = datetime.datetime.strptime(date_text, '%Y-%m-%d').date()
        except ValueError:
            flash('Please enter a valid date in YYYY-MM-DD format.', 'danger')
            return render_template('budget.html')
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
    if request.method == "POST":
        title = request.form.get('title')
        module_name = request.form.get('module_name')
        due_date_text = request.form.get('due_date') 
        priority = request.form.get('priority', "Medium")
        status = request.form.get('status', "Not started")
        notes = request.form.get('notes')
        if not title or not module_name or not due_date_text:
            flash("Title, module name and due date are required.", "danger")
            return redirect(url_for("assignments"))
        try:
            due_date = datetime.datetime.strptime(
                due_date_text,
                "%Y-%m-%d"
                ).date()
            
        except ValueError:
            flash("Please enter a date", "danger")
            return redirect (url_for("assignments"))
        
        assignment = Assignment(
            title=title,
            module_name=module_name,
            due_date=due_date,
            priority=priority,
            status=status,
            notes=notes,
            user_id=current_user.id
        )

        db.session.add(assignment)
        db.session.commit()


        flash("Assignment added successfully", "success")

        return redirect(url_for("assignments"))
    

    #====Assignment query return into summary==#
    selected_status = request.args.get("status")
    query = Assignment.query.filter_by(user_id=current_user.id)
    if selected_status:
        query = query.filter_by(status=selected_status)
    user_assignments = query.order_by(Assignment.due_date.asc()).all()
    return render_template(
            "assignments.html",
            assignments=user_assignments,
            selected_status=selected_status,
    )


#====Update and delete function for assignement cards - CRUD FUNCTION==#
#===Based on elements of https://flask-sqlalchemy.readthedocs.io/en/stable/queries==#
#=== and https://bdavison.napier.ac.uk/web/flask/basics/crud==#
@app.route("/assignment/<int:assignment_id>/status", methods=["POST"])
@login_required
def update_assignment_status(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    if assignment.user_id != current_user.id:
            flash("Not today, pal. You don't have permission to update this assignment.", "danger")
            return redirect(url_for("assignments"))
    new_status = request.form.get("status", "Not started")
    assignment.status = new_status
    db.session.commit()
    flash ("Well done, bucko. Assignment status updated.", "success")
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
        flash("Assignment torched.", "success")
        return redirect(url_for("assignments"))



   


if __name__ == '__main__':
    app.run(debug=True, port=5001)        