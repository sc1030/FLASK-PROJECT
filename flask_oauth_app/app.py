from flask import Flask, redirect, url_for, render_template
from flask_dance.contrib.google import make_google_blueprint, google
#from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
import os

app = Flask(__name__)
app.secret_key = os.getenv("", "supersecret")

# ✅ Google OAuth
google_bp = make_google_blueprint(
    client_id="",
    client_secret="",
    redirect_url="/google_login",
    scope=["profile", "email"]
)
app.register_blueprint(google_bp, url_prefix="/login")




# 🏠 Home
@app.route("/")
def index():
    return render_template("home.html")

# 🎯 Google Login Handler
@app.route("/google_login")
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v1/userinfo")
    return f"Google User: {resp.json()}"




if __name__ == "__main__":
    app.run(debug=True)
