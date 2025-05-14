from flask import Flask, render_template, request
import json
import urllib.request
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# List of categories
CATEGORIES = ['general', 'business', 'entertainment', 'health', 'science', 'sports', 'technology']

# List of countries (ISO 2-letter codes)
COUNTRIES = {
    'in': 'India',
    'us': 'USA',
    'gb': 'UK',
    'au': 'Australia',
    'ca': 'Canada',
    'fr': 'France',
    'de': 'Germany',
    'jp': 'Japan',
    'cn': 'China'
}

@app.route('/', methods=['GET', 'POST'])
def news():
    query = 'India'
    selected_category = None
    selected_country = 'in'  # default India
    page = request.args.get('page', 1, type=int)

    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        selected_category = request.form.get('category', '').strip()
        selected_country = request.form.get('country', 'in').strip()
        page = 1

    try:
        api_key = os.getenv('NEWS_API_KEY')
        if not api_key:
            return render_template('index.html', error="API Key not configured.", categories=CATEGORIES, countries=COUNTRIES)

        if selected_category:
            url = f"https://newsapi.org/v2/top-headlines?country={selected_country}&category={selected_category}&page={page}&pageSize=10&apiKey={api_key}"
        elif query:
            url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&page={page}&pageSize=10&apiKey={api_key}"
        else:
            url = f"https://newsapi.org/v2/top-headlines?country={selected_country}&page={page}&pageSize=10&apiKey={api_key}"

        with urllib.request.urlopen(url) as response:
            source = response.read()
            news_data = json.loads(source)

            if news_data['status'] != 'ok':
                return render_template('index.html', error="Failed to fetch news.", categories=CATEGORIES, countries=COUNTRIES)

            articles = news_data.get('articles', [])
            total_results = news_data.get('totalResults', 0)

            next_page = page + 1 if (page * 10) < total_results else None
            prev_page = page - 1 if page > 1 else None

            return render_template('index.html',
                                   articles=articles,
                                   query=query,
                                   categories=CATEGORIES,
                                   countries=COUNTRIES,
                                   selected_category=selected_category,
                                   selected_country=selected_country,
                                   page=page,
                                   next_page=next_page,
                                   prev_page=prev_page,
                                   total_results=total_results)

    except Exception as e:
        return render_template('index.html', error=f"Unexpected error: {e}", categories=CATEGORIES, countries=COUNTRIES)

if __name__ == "__main__":
    app.run(debug=True)
