from flask import Flask, render_template
app = Flask(__name__)

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
def dashboard():
    return render_template('dashboard.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/budget')
def budget():
    return render_template('budget.html')

@app.route('/assignments')
def assignments():
    return render_template('assignments.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001)        