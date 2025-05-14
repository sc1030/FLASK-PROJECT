from flask import Flask, render_template, request
from deep_translator import GoogleTranslator

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    translated_text = ""
    if request.method == 'POST':
        original_text = request.form['text']
        target_language = request.form['language']
        try:
            translated_text = GoogleTranslator(source='auto', target=target_language).translate(original_text)
        except Exception as e:
            translated_text = f"Error: {e}"
    return render_template('index.html', translated_text=translated_text)

if __name__ == '__main__':
    app.run(debug=True)
