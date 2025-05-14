from flask import Flask, render_template, request, flash, redirect
import requests

app = Flask(__name__)
app.secret_key = 'super-secret-key'  # for flashing messages

# 🔑 Replace with your actual keys from Google
RECAPTCHA_SITE_KEY = ''
RECAPTCHA_SECRET_KEY = ''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        captcha_response = request.form.get('g-recaptcha-response')

        # Send request to Google's verification API
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data={
            'secret': RECAPTCHA_SECRET_KEY,
            'response': captcha_response
        })

        result = r.json()
        print("CAPTCHA result:", result)

        if result.get('success'):
            flash('✅ CAPTCHA verified successfully!', 'success')
        else:
            flash('❌ CAPTCHA verification failed. Please try again.', 'danger')

        return redirect('/')

    return render_template('index.html', site_key=RECAPTCHA_SITE_KEY)

if __name__ == '__main__':
    app.run(debug=True)
