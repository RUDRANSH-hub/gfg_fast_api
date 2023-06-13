from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List
from db import SessionLocal, Prediction
from iris_model import model,iris

app = FastAPI()


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


@app.post("/predict")
def predict_species(data: IrisData, db=Depends(get_db)):
    input_data = [[data.sepal_length, data.sepal_width, data.petal_length, data.petal_width]]
    predictions = model.predict(input_data)
    species = iris.target_names[predictions[0]]

    prediction = Prediction(
        sepal_length=str(data.sepal_length),
        sepal_width=str(data.sepal_width),
        petal_length=str(data.petal_length),
        petal_width=str(data.petal_width),
        species=species
    )
    db.add(prediction)
    db.commit()

    return {"species": species}


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
