import uvicorn
from fastapi import FastAPI
from values import value
import numpy as np
import pickle
import pandas as pd
import json
import requests

app = FastAPI()
pickle_in = open("hyd_prices.pickle","rb")
model=pickle.load(pickle_in)
f = open('columns.json',)
data = data = json.load(f)
data_column = data['data_columns']
def get_estimated_price(property_size,bhk,property_age,gym,lift,swimmingPool,location):
    location = location.strip()
    gym = gym.strip()
    lift = lift.strip()
    swimmingPool = swimmingPool.strip()
    loc_index = data_column.index(location.lower())
    x = np.zeros(len(data_column))
    x[0] = property_size
    x[1] = bhk
    x[2] = property_age
    
    if gym == 'no':
        gym=0
    if gym == 'yes':
        gym=1
    x[3] = gym
    
    if lift == 'no':
        lift=0
    if lift == 'yes':
        lift=1
    x[4] = lift
    
    if swimmingPool == 'no':
        swimmingPool=0
    if swimmingPool == 'yes':
        swimmingPool=1
    x[5] = swimmingPool
    
    x[loc_index] = 1
    less = round(model.predict([x])[0],2)
    if less>= 35000 and bhk >= 3 and property_size >=2500 :
        less1 = less*2
        return less1
    else:
        return less


@app.get('/')
def index():
    return {'message': 'Hyderabad House Price Prediction made by natwar koneru'}

@app.post('/predict')
def predict_rent(data:value):
    data = data.dict()
    property_size= data['property_size']
    bhk= data['bhk']
    property_age= data['property_age']
    gym= data['gym']
    lift= data['lift']
    swimmingPool= data['swimmingPool']
    location= data['location']
    prediction = int(get_estimated_price(property_size,bhk,property_age,gym,lift,swimmingPool,location))
    
    return {
        'prediction': prediction
    }
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)

#uvicorn app:app --reload
