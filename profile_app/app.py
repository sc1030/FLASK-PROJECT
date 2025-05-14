from flask import Flask, render_template, request, redirect, url_for, session, flash
from db_config import get_db_connection
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = ''
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                       (name, email, password))
        conn.commit()
        conn.close()
        flash("Registration successful!", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user'] = user
            return redirect(url_for('profile'))
        else:
            flash("Invalid email or password", "danger")

    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('profile.html', user=session['user'])

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user' not in session:
        return redirect(url_for('login'))

    user_id = session['user']['id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        profile_pic = request.files['profile_pic']

        if profile_pic and profile_pic.filename != '':
            filename = secure_filename(profile_pic.filename)
            profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            cursor.execute("UPDATE users SET name=%s, contact=%s, profile_pic=%s WHERE id=%s",
                           (name, contact, filename, user_id))
        else:
            cursor.execute("UPDATE users SET name=%s, contact=%s WHERE id=%s",
                           (name, contact, user_id))

        conn.commit()
        flash('Profile updated successfully!')
        return redirect(url_for('profile'))

    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return render_template("edit_profile.html", user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
