from fastapi import FastAPI
from enum import Enum

app = FastAPI()

class FileType(str, Enum):
    jpg = "jpg"
    jpeg = "jpeg"
    lenet = "lenet"

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/history/current-inference")
async def read_current_history():
    return {"history_id": "the current user"}

@app.get("/history/all")
async def read_all_history():
    return {"history_id": ['id_list_and_data']}

@app.get("/history/{inference_id}")
async def specific_history(inference_id: int):
    return {"history_id": inference_id}