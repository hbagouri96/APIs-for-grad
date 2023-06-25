from flask import Flask,request,jsonify
import util

app = Flask(__name__)


@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    area = float(request.form['area'])
    location = request.form['location']
    bedrooms = int(request.form['bedrooms'])
    bathrooms = int(request.form['bathrooms'])

    response = jsonify({
        'estimated_price': util.get_estimated_price(location,area,bedrooms,bathrooms)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

if __name__ == "__main__":
    print("start Flask server")
    app.run(debug=True)