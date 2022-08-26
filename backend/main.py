import os
import aiofiles
import zipfile
from io import BytesIO
from fastapi import FastAPI, File, UploadFile, HTTPException, responses
from fastapi.middleware.cors import CORSMiddleware
from enum import Enum
from sqlalchemy import text, select
from db import db, tables
from middleware import LimitUploadSize

WORKSPACE = os.environ.get('WORKSPACE')

INPUT_IMG_PATH = "{}/image-dataset/highres-img".format(WORKSPACE)
CROP_IMG_PATH = "{}/image-dataset/cropped-img".format(WORKSPACE)
SUPER_IMG_PATH = "{}/image-dataset/super-result".format(WORKSPACE)

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://localhost:3000",
]

# REGISTER MIDDLEWARE
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LimitUploadSize, max_upload_size=10_000_000) #10mb

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
async def inference(file: UploadFile = File(...)):
    if file.content_type != "image/jpeg":
        raise HTTPException(status_code=415, detail="Only support .jpg file")

    output_file = "{}/{}".format(INPUT_IMG_PATH, file.filename) #ganti nama file 
    async with aiofiles.open(output_file, 'wb') as out_file:
        query = "INSERT INTO tbl_img_input (img_path) VALUES ('{}')".format(file.filename)
        results = db.engine.execute(query)

        content = await file.read()
        await out_file.write(content)

    return {"filename": file.filename, "results": results}

@app.get("/history/all")
async def read_all_history():
    return {"history_id": ['id_list_and_data']}

@app.get("/history/{inference_id}")
async def specific_history(inference_id: int):
    return {"history_id": inference_id}

@app.get('/image')
def get_all_image_path():
    query = select(tables.tbl_img_input)
    results = db.engine.execute(query).fetchall()
    payload = []
    for row in results:
        payload.append(row)
    return payload

@app.get('/image/{image_id}')
def get_image(image_id):
    query = select(tables.tbl_img_input).where(tables.tbl_img_input.c.id==image_id)
    result = db.engine.execute(query).fetchone()

    if not result:
        raise HTTPException(status_code=400, detail="File not found")
    
    file_location = "{}/{}".format(INPUT_IMG_PATH, result[1])
    
    return responses.FileResponse(file_location)

@app.get('/zip-image/{image_ids}')
def get_zip_image(image_ids):    
    ids = tuple(map(int, image_ids.split(",")))
    query = select(tables.tbl_img_input).filter(tables.tbl_img_input.c.id.in_(ids))
    results = db.engine.execute(query).fetchall()

    if not results:
        return {"results": []}
    
    file_list = []
    for result in results:
        file_path = "{}/{}".format(INPUT_IMG_PATH, result[1])
        file_exists = os.path.exists(file_path)
        if file_exists:
            file_list.append(file_path)

    io = BytesIO()
    zip_sub_dir = "multiple-img"
    zip_filename = "%s.zip" % zip_sub_dir
    with zipfile.ZipFile(io, mode='w', compression=zipfile.ZIP_DEFLATED) as zip:
        for fpath in file_list:
            zip.write(fpath)
        zip.close()
    return responses.StreamingResponse(
        iter([io.getvalue()]),
        media_type="application/x-zip-compressed",
        headers = { "Content-Disposition":f"attachment;filename=%s" % zip_filename}
    )
    
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
