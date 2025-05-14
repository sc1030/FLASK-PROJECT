from flask import Flask, request, jsonify
from flask import render_template
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')
# Sample data - in a real app, this would come from a database
SUGGESTION_DATA = [
    "apple", "apricot", "avocado",
    "banana", "blueberry", "blackberry",
    "cherry", "coconut", "cranberry",
    "date", "dragonfruit",
    "elderberry",
    "fig",
    "grape", "grapefruit", "guava",
    "kiwi",
    "lemon", "lime", "lychee",
    "mango", "melon",
    "orange",
    "papaya", "peach", "pear", "pineapple", "plum", "pomegranate",
    "raspberry",
    "strawberry",
    "tangerine",
    "watermelon"
]

@app.route('/suggest', methods=['GET'])
def suggest():
    query = request.args.get('query', '').lower()
    if not query:
        return jsonify([])
    
    # Filter suggestions that start with the query
    suggestions = [item for item in SUGGESTION_DATA if item.startswith(query)]
    
    # For more flexible matching (contains the query anywhere):
    # suggestions = [item for item in SUGGESTION_DATA if query in item]
    
    return jsonify(suggestions[:10])  # Limit to 10 suggestions

if __name__ == '__main__':
    app.run(debug=True)