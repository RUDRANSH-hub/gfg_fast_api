from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel
import pickle
# from joblib import load

app = FastAPI()
pickle_in=open("titanic_model.pkl","rb")
clf=pickle.load(pickle_in)
   
class Passenger(BaseModel):
    pclass: int
    age: float
    sibsp: int
    parch: int
    fare: float

@app.get('/')
def index():
    return {'message':'Welcome to App'}





@app.post("/predict")
def predict_passenger_survival(data:Passenger):
    
    prediction=clf.predict([[data.pclass,data.age,data.sibsp,data.parch,data.fare]])
    
    return {
        'prediction': int(prediction[0])
    }

