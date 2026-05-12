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
from models import User, db

load_dotenv()

app = Flask(__name__)

#====CONFIG====#

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
print(os.environ.get("DATABASE_URL"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    

#====DATABSE INIT====#
db.init_app(app)

with app.app_context():
    db.create_all() 
    print('Database tables created successfully.')  

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


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


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

        print(f"EMAIL: {email}")
        print(f"PASSWORD: {password}")  # Debugging line

        user = User.query.filter_by(email=email).first()

        print(f"USER: {user}")  # Debugging line

        if user:
            print(f"PASSWORD CHECK: {len(user.password_hash)}")  # Debugging line
       
            print(f"HASH LENGTH: {len(user.password_hash)  }")  # Debugging line
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful! Welcome back.', 'success')
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

@app.route('/budget')
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
            expense_date = datetime.strptime(date_text, '%Y-%m-%d').date()
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





    return render_template('budget.html')

@app.route('/assignments')
def assignments():
    return render_template('assignments.html')


if __name__ == '__main__':
    app.run(debug=True)        