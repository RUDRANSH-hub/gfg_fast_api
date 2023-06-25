from fastapi import FastAPI, Request,Depends,Form
from typing import Any
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import joblib
import numpy as np
from count_vec import prediction
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")
# Load the trained model and important models
model = joblib.load('spam_ham.joblib')

class Email(BaseModel):
    body: str
@app.get("/")
def index(request:Request):
    return templates.TemplateResponse("index.html",{"request":request,"label":None,"Not_Spam":None,"spam":None})
# Define the API route for email classification
@app.post("/Classify")
async def classify_email(request:Request,text: str=Form(...)):
    
    t_dtv=prediction(text)
    res=('Spam' if model.predict(t_dtv)[0] else 'Not_Spam')
    prob = model.predict_proba(t_dtv)*100
    # Return the prediction as the API response
    # return {'label': str(res),'Not Spam':prob[0][0],'spam':prob[0][1]}
    return templates.TemplateResponse("index.html",{"request":request,"label":res,"Not_Spam":prob[0][0],"spam":prob[0][1]})


