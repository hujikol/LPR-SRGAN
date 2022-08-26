import aiofiles
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from enum import Enum
from sqlalchemy import text
from db import db

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

input_img_path = "/image-dataset/highres-img/"
crop_img_path = "/image-dataset/cropped-img"
super_img_path = "/image-dataset/super-result"

@app.on_event("startup")
async def startup():
    await db.database.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.database.disconnect()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/inference")
async def inference(in_file: UploadFile=File(...)):
    async with aiofiles.open(input_img_path, 'wb') as out_file:
        content = await in_file.read()
        await out_file.write(content)

    return {"Result": "OK"}


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
    return payload

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
