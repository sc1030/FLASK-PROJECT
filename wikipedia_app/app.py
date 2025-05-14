from flask import Flask, render_template, request, jsonify
import wikipedia

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def ajax_search():
    data = request.get_json()
    query = data.get('query')
    lang = data.get('lang', 'en')
    wikipedia.set_lang(lang)

    try:
        page = wikipedia.page(query)
        return jsonify({
            'title': page.title,
            'summary': page.summary,
            'image': page.images[0] if page.images else '',
            'url': page.url,
            'toc': page.sections
        })
    except wikipedia.exceptions.DisambiguationError as e:
        return jsonify({'error': f"Disambiguation: Try one of these - {', '.join(e.options[:5])}"})
    except wikipedia.exceptions.PageError:
        return jsonify({'error': "Page not found."})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
