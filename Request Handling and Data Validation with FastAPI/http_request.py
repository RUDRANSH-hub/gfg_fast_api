# FastAPI provides decorators like @app.get() and @app.post() to 
# handle HTTP requests. These decorators allow you to define the 
# endpoint paths and specify the HTTP methods to handle. Here's an example:

from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

