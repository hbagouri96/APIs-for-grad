import requests
from bs4 import BeautifulSoup
from flask import Flask,request,jsonify
import util
import urllib.request
import re

app = Flask(__name__)


@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

def predict_home_price(details):
    area = float(details['area'])
    location = details['location']
    bedrooms = int(details['bedrooms'])
    bathrooms = int(details['bathrooms'])

    
    return util.get_estimated_price(location,area,bedrooms,bathrooms)

@app.route('/dubizzlescrape', methods=['POST'])
def scrape_property():
    data = request.get_json()
    url = data['url']
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Scrape location
    location_element = soup.find('span', attrs={'aria-label': 'Location'})
    location = location_element.text.strip()

    # Scrape area, bedrooms, and bathrooms
    details_element = soup.find('div', attrs={'aria-label': 'Details'})
    area = int(details_element.find('span', text='Area (m²)').find_next_sibling('span').text.replace(',', ''))
    bedrooms = int(details_element.find('span', text='Bedrooms').find_next_sibling('span').text)
    bathrooms = int(details_element.find('span', text='Bathrooms').find_next_sibling('span').text)

    # Prepare the response
    response_data = {
        'location': location,
        'area': area,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms
    }

    return jsonify({
        'price': predict_home_price(response_data),
        'location': location,
        'area': area,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms
    })

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
        prediction_data = {
            'location': location,
            'area': area_value,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms
        }
        return jsonify({
            'price': predict_home_price(prediction_data),
            'location': location,
            'area': area_value,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms
        })
    except Exception as e:
        # Return error message if any exception occurs during scraping
        return jsonify({'error': str(e)}), 500

# if __name__ == "__main__":
#     print("start Flask server")
#     app.run()
