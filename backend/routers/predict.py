import aiofiles
import zipfile 

from io import BytesIO
from fastapi import APIRouter, File, UploadFile, HTTPException, responses
from sqlalchemy import select
from db import db, tables
from utils import variables, preprocess

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.post("/inference")
async def inference(file: UploadFile = File(...)):
    if file.content_type != "image/jpeg":
        raise HTTPException(status_code=415, detail="Only support .jpg file")

    output_file = "{}/{}".format(variables.INPUT_IMG_PATH, file.filename) #ganti nama file 
    async with aiofiles.open(output_file, 'wb') as out_file:
        query = "INSERT INTO tbl_img_input (img_path) VALUES ('{}')".format(file.filename)
        results = db.engine.execute(query)

        content = await file.read()
        await out_file.write(content)

    return {"filename": file.filename, "results": results}

@router.get("/history/all")
async def read_all_history():
    return {"history_id": ['id_list_and_data']}

@router.get("/history/{inference_id}")
async def specific_history(inference_id: int):
    return {"history_id": inference_id}

@router.get('/image')
def get_all_image_path():
    query = select(tables.tbl_img_input)
    results = db.engine.execute(query).fetchall()
    payload = []
    for row in results:
        payload.append(row)
    return payload

@router.get('/image/{image_id}')
def get_image(image_id):
    query = select(tables.tbl_img_input).where(tables.tbl_img_input.c.id==image_id)
    result = db.engine.execute(query).fetchone()

    if not result:
        raise HTTPException(status_code=400, detail="File not found")
    
    file_location = "{}/{}".format(variables.INPUT_IMG_PATH, result[1])
    
    return responses.FileResponse(file_location)

@router.get('/zip-image/{image_ids}')
def get_zip_image(image_ids):    
    ids = tuple(map(int, image_ids.split(",")))
    query = select(tables.tbl_img_input).filter(tables.tbl_img_input.c.id.in_(ids))
    results = db.engine.execute(query).fetchall()

    if not results:
        return {"results": []}
    
    file_list = []
    for result in results:
        file_path = "{}/{}".format(variables.INPUT_IMG_PATH, result[1])
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