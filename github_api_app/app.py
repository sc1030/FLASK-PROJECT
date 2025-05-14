from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

GITHUB_API_URL = ""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/github-user', methods=['POST'])
def get_github_user():
    username = request.json.get('username')
    if not username:
        return jsonify({'error': 'Username is required'}), 400

    response = requests.get(GITHUB_API_URL + username)

    if response.status_code != 200:
        return jsonify({'error': 'GitHub user not found'}), 404

    data = response.json()
    result = {
        'username': data.get('login'),
        'avatar_url': data.get('avatar_url'),
        'public_repos': data.get('public_repos')
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
