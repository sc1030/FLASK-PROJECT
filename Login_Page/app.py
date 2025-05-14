from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this in production

# MySQL Config
app.config['MYSQL_HOST'] = ''
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''  # Set your MySQL password
app.config['MYSQL_DB'] = ''
app.config['MYSQL_CURSORCLASS'] = ''

mysql = MySQL(app)

@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_pw = generate_password_hash(password)

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cur.fetchone()
        if user:
            flash("Email already exists!", "error")
        else:
            cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                        (username, email, hashed_pw))
            mysql.connection.commit()
            flash("Registration successful!", "success")
            return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cur.fetchone()

        if user and check_password_hash(user['password'], password):
            session['loggedin'] = True
            session['username'] = user['username']
            return redirect('/dashboard')
        else:
            flash("Invalid credentials!", "error")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect('/login')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
