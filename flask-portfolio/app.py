from flask import Flask, render_template, request, redirect, url_for
from email.message import EmailMessage
import smtplib

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sendemail/", methods=["POST"])
def sendemail():
    if request.method == "POST":
        name = request.form["name"]
        subject = request.form["Subject"]
        email = request.form["_replyto"]
        message = request.form["message"]

        # Your Gmail credentials
        your_email = "your_email@gmail.com"
        your_password = "your_app_password"

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(your_email, your_password)

        msg = EmailMessage()
        msg.set_content(f"Name: {name}\nEmail: {email}\nSubject: {subject}\nMessage: {message}")
        msg["To"] = your_email
        msg["From"] = your_email
        msg["Subject"] = subject

        try:
            server.send_message(msg)
            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")

        server.quit()
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
