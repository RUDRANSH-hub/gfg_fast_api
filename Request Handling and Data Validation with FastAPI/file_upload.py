from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.post("/files/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {"filename": file.filename, "contents": contents}
