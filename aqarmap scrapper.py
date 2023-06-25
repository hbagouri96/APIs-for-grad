from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import urllib.request
import re

app = Flask(__name__)

@app.route('/aqarmapscrape', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data['url']

    try:
        # Create the request object with headers
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)

        # Make the HTTP request using urllib
        with urllib.request.urlopen(req) as response:
            html = response.read()

        soup = BeautifulSoup(html, 'html.parser')

        # Extract the location
        location_element = soup.find('a', class_='text-inherit')
        location = location_element.get_text(strip=True) if location_element else None

        # Extract the area
        area_element = soup.find(lambda tag: tag.name == 'span' and 'Size (in meters)' in tag.text)
        area_text = area_element.find_next_sibling('span').get_text(strip=True) if area_element else None
        area_value = int(re.findall(r'\d+', area_text)[0]) if area_text else None

        # Extract the bedrooms
        bedrooms_element = soup.find(lambda tag: tag.name == 'span' and 'Room' in tag.text)
        bedrooms = int(bedrooms_element.find_next_sibling('span').get_text(strip=True)) if bedrooms_element else None

        # Extract the bathrooms
        bathrooms_element = soup.find(lambda tag: tag.name == 'span' and 'Baths' in tag.text)
        bathrooms = int(bathrooms_element.find_next_sibling('span').get_text(strip=True)) if bathrooms_element else None

        # Return the scraped data as a JSON response
        return jsonify({
            'location': location,
            'area': area_value,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms
        })
    except Exception as e:
        # Return error message if any exception occurs during scraping
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
