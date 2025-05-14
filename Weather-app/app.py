from flask import Flask, render_template, request
import json
import urllib.request
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def weather():
    # Default city
    city = 'mathura'
    
    if request.method == 'POST':
        city = request.form.get('city', 'mathura').strip()
    
    try:
        # Get API key from environment variable
        api_key = os.getenv('OPENWEATHER_API_KEY')
        if not api_key:
            return render_template('index.html', 
                                 error="API key not configured. Please contact administrator.")
        
        # Create properly formatted URL (removed spaces around =)
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        
        # Make API request
        with urllib.request.urlopen(url) as response:
            source = response.read()
            list_of_data = json.loads(source)

            # Process weather data
            data = {
                "city": city,
                "country_code": list_of_data['sys']['country'],
                "coordinates": {
                    "lon": list_of_data['coord']['lon'],
                    "lat": list_of_data['coord']['lat']
                },
                "temp": round(list_of_data['main']['temp'], 1),
                "temp_unit": "°C",
                "feels_like": round(list_of_data['main']['feels_like'], 1),
                "pressure": list_of_data['main']['pressure'],
                "humidity": list_of_data['main']['humidity'],
                "weather": {
                    "main": list_of_data['weather'][0]['main'],
                    "description": list_of_data['weather'][0]['description'],
                    "icon": list_of_data['weather'][0]['icon']
                },
                "wind": {
                    "speed": list_of_data['wind']['speed'],
                    "deg": list_of_data['wind'].get('deg', 'N/A')
                }
            }
            
            return render_template('index.html', data=data)
            
    except urllib.error.HTTPError as e:
        error_msg = f"API Error: {e.code}"
        if e.code == 401:
            error_msg = "Invalid API Key. Please check your configuration."
        elif e.code == 404:
            error_msg = f"City '{city}' not found."
        return render_template('index.html', error=error_msg)
        
    except urllib.error.URLError as e:
        return render_template('index.html', error=f"Network Error: {e.reason}")
        
    except KeyError as e:
        return render_template('index.html', error=f"Unexpected API response format. Missing key: {e}")
        
    except Exception as e:
        return render_template('index.html', error=f"Unexpected error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)