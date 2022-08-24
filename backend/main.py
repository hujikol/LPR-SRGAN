from fastapi import FastAPI
from enum import Enum
from sqlalchemy import text
from db import db

app = FastAPI()

@app.on_event("startup")
async def startup():
    await db.database.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.database.disconnect()

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

@app.get('/image')
def get_all_image_path():
    query = text("SELECT * FROM tbl_img_input")
    results = db.engine.execute(query)    
    payload = []
    for row in results:
        payload.append(row)    
    return {"result": payload}

@app.get('/cobainput')
def coba_input():
    datas = [
        {"img_path": 'asd.png'},
        {"img_path": '123.png'},
    ]
    for data in datas:
        query = text("INSERT INTO tbl_img_input (img_path) VALUES ('{}')".format(data['img_path']))
        db.engine.execute(query)
    
    return {"result": True}
