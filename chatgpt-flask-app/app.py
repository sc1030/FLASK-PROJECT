from flask import Flask, render_template, request, jsonify
import cohere
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Initialize Cohere client
cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    try:
        response = cohere_client.chat(
            message=user_input,
            model="command-r"
        )
        reply = response.text.strip()
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
