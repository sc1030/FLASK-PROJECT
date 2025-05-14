from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Sample data to simulate a database
data = [
    "Apple", "Banana", "Cherry", "Date", "Elderberry", "Fig", "Grape",
    "Honeydew", "Indian Fig", "Jackfruit", "Kiwi", "Lemon", "Mango"
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query', '').lower()
    results = [item for item in data if query in item.lower()]
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
