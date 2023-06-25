import pickle
import json
import numpy as np

__locations = None
__data_columns = None
__model = None

def get_estimated_price(location,area,bedrooms,bathrooms):
    load_saved_artifacts()
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = bedrooms
    x[1] = bathrooms
    x[2] = area
    if loc_index>=0:
        x[loc_index] = 1

    return round(__model.predict([x])[0],-3)


def load_saved_artifacts():
    print("loading saved artifacts...start")
    global  __data_columns
    global __locations
    global __model

    with open("./artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]  

    if __model is None:
        with open('./artifacts/egypt_price_prediction_model.pickle', 'rb') as f:
            __model = pickle.load(f)
    print("loading saved artifacts...done")

def get_location_names():
    load_saved_artifacts()
    return __locations

def get_data_columns():
    load_saved_artifacts()
    return __data_columns

if __name__ == '__main__':
    load_saved_artifacts()