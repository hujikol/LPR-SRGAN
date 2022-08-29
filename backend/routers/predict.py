import aiofiles
import zipfile 
from sqlalchemy.orm import Session
from io import BytesIO
from fastapi import APIRouter, File, UploadFile, HTTPException, responses
from sqlalchemy import select
from db import db, tables
from utils import variables

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.post("/upload-img")
async def upload_img(file: UploadFile = File(...)):
    if file.content_type != "image/jpeg":
        raise HTTPException(status_code=415, detail="Only support .jpg or .jpeg file")

    filename = file.filename
    output_file = "{}/{}".format(variables.INPUT_IMG_PATH, filename) #ganti nama file 
    async with aiofiles.open(output_file, 'wb') as out_file:
        img_input_obj = db.ImgInput(img_path=filename)
        with Session(db.engine) as session:
            session.add(img_input_obj)
            session.commit()
            
            img_id = img_input_obj.id
            img_path = img_input_obj.img_path
            
            session.close()

        content = await file.read()
        await out_file.write(content)

    return {"id": img_id, "img_path": img_path}

@router.post("/predict/{img_id}")
async def predict(img_id):
    query = select(db.ImgInput).where(db.ImgInput.id==img_id)
    with Session(db.engine) as session:
        result = session.execute(query).fetchone()[0]
        session.close()
    if not result:
        raise HTTPException(status_code=400, detail="Image id not found")
    
    # result.img_path will return filename
    # CALL PREDICT HERE
    return {"success": 200}


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