from fastapi import FastAPI, Depends,Request,Form
from pydantic import BaseModel
from typing import List
from db import SessionLocal, Prediction
from iris_model import model,iris
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")

class IrisData(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


class PredictionData(IrisData):
    species: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def index(request:Request):
    
    return templates.TemplateResponse("index.html",{"request":request,"species":None})
@app.post("/predict")

async def predict_species(request: Request, sepal_length: float = Form(...), sepal_width: float = Form(...), petal_length: float = Form(...), petal_width: float = Form(...), db=Depends(get_db)):
    input_data = [[sepal_length, sepal_width, petal_length, petal_width]]
    predictions = model.predict(input_data)
    species = iris.target_names[predictions[0]]

    prediction = Prediction(
        sepal_length=str(sepal_length),
        sepal_width=str(sepal_width),
        petal_length=str(petal_length),
        petal_width=str(petal_width),
        species=species
    )
    db.add(prediction)
    db.commit()

    return templates.TemplateResponse("index.html", {"request": request, "species": species})


@app.get("/predictions", response_model=List[PredictionData])
def get_predictions(db=Depends(get_db)):
    predictions = db.query(Prediction).all()
    return [
        PredictionData(
            sepal_length=p.sepal_length,
            sepal_width=p.sepal_width,
            petal_length=p.petal_length,
            petal_width=p.petal_width,
            species=p.species
        )
        for p in predictions
    ]
