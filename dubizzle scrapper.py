import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request

app = Flask(__name__)

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

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
