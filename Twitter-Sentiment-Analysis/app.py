from flask import Flask, render_template, request, redirect, url_for, flash, session
from sentiments import analyze_sentiment, save_to_csv
import os
import csv

app = Flask(__name__)
app.secret_key = ''

# ✅ Route for root ("/") — redirects to login
@app.route('/')
def index():
    return redirect(url_for('login'))

# Route for registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if user already exists
        if os.path.exists('users.csv'):
            with open('users.csv', 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row and row[0] == username:
                        flash('Username already exists. Try a different one.')
                        return redirect(url_for('register'))

        # Save to users.csv
        with open('users.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([username, password])

        flash('Registration successful! Please login.')
        return redirect(url_for('login'))

    return render_template('register.html')

# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check credentials against users.csv
        if os.path.exists('users.csv'):
            with open('users.csv', 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row and row[0] == username and row[1] == password:
                        session['username'] = username
                        return redirect(url_for('home'))

        flash('Invalid credentials. Please try again.')
        return redirect(url_for('login'))

    return render_template('login.html')

# Home route
@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        keyword = request.form['search_term']
        num_tweets = int(request.form['tweet_count'])  # Convert the input to integer

        # Perform sentiment analysis
        tweet_data = analyze_sentiment(keyword, num_tweets)
        save_to_csv(tweet_data)
        
        return render_template('sentiment_analyzer.html', data=tweet_data)
    
    return render_template('sentiment_analyzer.html')


# Pie chart route
@app.route('/piechart')
def piechart():
    return render_template('PieChart.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
