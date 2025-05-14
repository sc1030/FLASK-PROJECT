from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('mailfinder.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    email_results = []
    if request.method == 'POST':
        name_query = request.form['full_name'].strip().lower()
        conn = get_db_connection()
        cursor = conn.execute("SELECT email FROM users WHERE LOWER(full_name) LIKE ?", ('%' + name_query + '%',))
        email_results = [row['email'] for row in cursor.fetchall()]
        conn.close()
    return render_template('index.html', email_results=email_results)

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('q', '').strip().lower()
    conn = get_db_connection()
    cursor = conn.execute("SELECT full_name FROM users WHERE LOWER(full_name) LIKE ?", ('%' + query + '%',))
    suggestions = [row['full_name'] for row in cursor.fetchall()]
    conn.close()
    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True)
