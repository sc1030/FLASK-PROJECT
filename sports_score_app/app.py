# app.py
from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import logging
from urllib.parse import urlencode

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cache setup
CACHE_DURATION = 300  # 5 minutes
cache = {
    'live': {'time': 0, 'data': None},
    'upcoming': {'time': 0, 'data': None},
    'past': {'time': 0, 'data': None}
}

def get_soup(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    session = requests.Session()
    session.headers.update(headers)
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching {url}: {e}")
        return None

def scrape_live_matches():
    current_time = time.time()
    if current_time - cache['live']['time'] < CACHE_DURATION and cache['live']['data']:
        return cache['live']['data']

    soup = get_soup("https://www.cricbuzz.com/cricket-match/live-scores")
    if not soup:
        return None

    matches = []
    for match in soup.find_all('div', class_='cb-mtch-lst'):
        try:
            title = match.find('h3').get_text(strip=True) if match.find('h3') else "No Title"
            teams = match.find_all('div', class_='cb-ovr-flo')
            status = match.find('div', class_='cb-text-live').get_text(strip=True) if match.find('div', class_='cb-text-live') else "No Status"
            link = match.find('a')['href'] if match.find('a') else "#"

            matches.append({
                'title': title,
                'team1': teams[0].get_text(strip=True) if len(teams) > 0 else "N/A",
                'team2': teams[1].get_text(strip=True) if len(teams) > 1 else "N/A",
                'status': status,
                'link': f"https://www.cricbuzz.com{link}"
            })
        except Exception as e:
            logger.error(f"Error parsing live match: {e}")

    cache['live']['data'] = matches
    cache['live']['time'] = current_time
    return matches

def scrape_upcoming_matches():
    current_time = time.time()
    if current_time - cache['upcoming']['time'] < CACHE_DURATION and cache['upcoming']['data']:
        return cache['upcoming']['data']

    soup = get_soup("https://www.cricbuzz.com/cricket-match/live-scores/upcoming-matches")
    if not soup:
        return None

    matches = []
    for match in soup.find_all('div', class_='cb-mtch-lst'):
        try:
            title = match.find('h3').get_text(strip=True) if match.find('h3') else "No Title"
            teams = match.find_all('div', class_='cb-ovr-flo')
            date = match.find('div', class_='text-gray').get_text(strip=True) if match.find('div', class_='text-gray') else "No Date"
            link = match.find('a')['href'] if match.find('a') else "#"

            matches.append({
                'title': title,
                'team1': teams[0].get_text(strip=True) if len(teams) > 0 else "N/A",
                'team2': teams[1].get_text(strip=True) if len(teams) > 1 else "N/A",
                'date': date,
                'link': f"https://www.cricbuzz.com{link}"
            })
        except Exception as e:
            logger.error(f"Error parsing upcoming match: {e}")

    cache['upcoming']['data'] = matches
    cache['upcoming']['time'] = current_time
    return matches

def scrape_past_matches():
    current_time = time.time()
    if current_time - cache['past']['time'] < CACHE_DURATION and cache['past']['data']:
        return cache['past']['data']

    soup = get_soup("https://www.cricbuzz.com/cricket-match/live-scores/recent-matches")
    if not soup:
        return None

    matches = []
    for match in soup.find_all('div', class_='cb-mtch-lst'):
        try:
            title = match.find('h3').get_text(strip=True) if match.find('h3') else "No Title"
            teams = match.find_all('div', class_='cb-ovr-flo')
            result = match.find('div', class_='cb-text-complete').get_text(strip=True) if match.find('div', class_='cb-text-complete') else "No Result"
            link = match.find('a')['href'] if match.find('a') else "#"

            matches.append({
                'title': title,
                'team1': teams[0].get_text(strip=True) if len(teams) > 0 else "N/A",
                'team2': teams[1].get_text(strip=True) if len(teams) > 1 else "N/A",
                'result': result,
                'link': f"https://www.cricbuzz.com{link}"
            })
        except Exception as e:
            logger.error(f"Error parsing past match: {e}")

    cache['past']['data'] = matches
    cache['past']['time'] = current_time
    return matches

def scrape_match_details(match_url):
    soup = get_soup(match_url)
    if not soup:
        return None

    try:
        match_data = {
            'match_info': {},
            'scorecard': {},
            'fall_of_wickets': [],
            'commentary': [],
            'innings': []
        }

        # Match Info
        match_title = soup.find('h1', class_='cb-nav-hdr')
        if match_title:
            match_data['match_info']['title'] = match_title.get_text(strip=True)

        teams = soup.find_all('span', class_='cb-font-20')
        if len(teams) >= 2:
            match_data['match_info']['team1'] = teams[0].get_text(strip=True)
            match_data['match_info']['team2'] = teams[1].get_text(strip=True)

        venue = soup.find('span', itemprop='name')
        if venue:
            match_data['match_info']['venue'] = venue.get_text(strip=True)

        date = soup.find('span', class_='cb-font-12')
        if date:
            match_data['match_info']['date'] = date.get_text(strip=True)

        # Scorecard
        for section in soup.find_all('div', class_='cb-col cb-col-100 cb-ltst-wgt-hdr'):
            heading = section.find('h2')
            if heading:
                heading_text = heading.get_text(strip=True)
                if 'Innings' in heading_text:
                    headers = []
                    header_row = section.find('div', class_='cb-col cb-col-100 cb-scrd-hdr-rw')
                    if header_row:
                        headers = [th.get_text(strip=True) for th in header_row.find_all('div')]
                    
                    rows = []
                    for row in section.find_all('div', class_='cb-col cb-col-100 cb-scrd-itms'):
                        cells = []
                        for cell in row.find_all('div', recursive=False):
                            cell_text = cell.get_text(strip=True)
                            if cell_text:  # Only add non-empty cells
                                cells.append(cell_text)
                        if cells:  # Only add non-empty rows
                            rows.append(cells)
                    
                    if headers or rows:  # Only add if we have data
                        match_data['scorecard'][heading_text] = {
                            'headers': headers,
                            'rows': rows
                        }

        # Fall of Wickets
        fow_section = soup.find('div', string='Fall of Wickets')
        if fow_section:
            fow_parent = fow_section.find_parent('div', class_='cb-col cb-col-100 cb-minfo-tm-nm')
            if fow_parent:
                fow_text = fow_parent.get_text(strip=True).replace('Fall of Wickets', '')
                match_data['fall_of_wickets'] = [w.strip() for w in fow_text.split(',') if w.strip()]

        # Commentary
        commentary_section = soup.find('div', class_='cb-col cb-col-100 cb-min-hgt cb-com-lst')
        if commentary_section:
            for item in commentary_section.find_all('div', class_='cb-min-com'):
                over = item.find('span', class_='cb-com-ov')
                text = item.find('div', class_='cb-com-ln')
                if over and text:
                    timestamp = item.find('div', class_='cb-col cb-col-10 cb-com-dt')
                    match_data['commentary'].append({
                        'over': over.get_text(strip=True),
                        'text': text.get_text(strip=True),
                        'timestamp': timestamp.get_text(strip=True) if timestamp else ''
                    })

        # Innings
        innings_sections = soup.find_all('div', class_='cb-col cb-col-100 cb-scrd-itms')
        for section in innings_sections:
            if 'Innings' in section.get_text():
                match_data['innings'].append(section.get_text(strip=True))

        return match_data

    except Exception as e:
        logger.error(f"Error parsing match details: {e}")
        return None

@app.route('/')
def home():
    live = scrape_live_matches() or []
    upcoming = scrape_upcoming_matches() or []
    past = scrape_past_matches() or []
    return render_template('index.html', 
                         live_matches=live,
                         upcoming_matches=upcoming,
                         past_matches=past,
                         datetime=datetime)

@app.route('/match')
def match_details():
    match_url = request.args.get('url')
    if not match_url:
        return render_template('error.html', message="Match URL not provided"), 400

    details = scrape_match_details(match_url)
    if not details:
        return render_template('error.html', message="Failed to fetch match details"), 500

    return render_template('match.html', 
                         match_info=details['match_info'],
                         scorecard=details['scorecard'],
                         commentary=details['commentary'],
                         fall_of_wickets=details['fall_of_wickets'],
                         innings=details['innings'])

@app.route('/api/live')
def api_live():
    return jsonify(scrape_live_matches() or [])

@app.route('/api/upcoming')
def api_upcoming():
    return jsonify(scrape_upcoming_matches() or [])

@app.route('/api/past')
def api_past():
    return jsonify(scrape_past_matches() or [])

@app.route('/api/match')
def api_match():
    match_url = request.args.get('url')
    if not match_url:
        return jsonify({'error': 'Match URL not provided'}), 400

    details = scrape_match_details(match_url)
    if not details:
        return jsonify({'error': 'Failed to fetch match details'}), 500

    return jsonify(details)

@app.route('/error')
def error():
    message = request.args.get('message', 'An error occurred')
    return render_template('error.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)