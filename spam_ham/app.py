from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import joblib
import numpy as np
from count_vec import prediction
app = FastAPI()

# Load the trained model and important models
model = joblib.load('spam_ham.joblib')

class Email(BaseModel):
    body: str

# Define the API route for email classification
@app.post("/classify")
async def classify_email(email: Email):
    text = email.body
    t_dtv=prediction(text)
    res=('Spam' if model.predict(t_dtv)[0] else 'Not Spam')
    prob = model.predict_proba(t_dtv)*100
    # Return the prediction as the API response
    return {'label': str(res),'Not Spam':prob[0][0],'spam':prob[0][1]}


