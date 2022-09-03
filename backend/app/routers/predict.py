import aiofiles
import zipfile 
import time
import subprocess

from sqlalchemy.orm import Session
from io import BytesIO
from fastapi import APIRouter, File, UploadFile, HTTPException, responses
from sqlalchemy import select
from db import db, tables
from utils import variables, preprocess, bounding_box

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
            
            session.close()

        content = await file.read()
        await out_file.write(content)

    return {"id": img_id}

# get img bounding-box and save to db BoundingBox
@router.post("/get-bounding-box/{img_id}")
async def get_bounding_box(img_id):
    query = select(db.ImgInput).where(db.ImgInput.id==img_id)
    with Session(db.engine) as session:
        result = session.execute(query).fetchone()[0]
        img_path = result.img_path
        
        session.close()
    if not result:
        raise HTTPException(status_code=400, detail="Image id not found")
    
    img_path = variables.INPUT_IMG_PATH + "/" + img_path
    
    # call darknet to run yolov4
    # !./darknet detector test <LPR/obj.data> <LPR/darknet/yolov4-obj.cfg> <LPR/detectionBKP/yolov4-obj_last.weights> -ext_output <LPR/testingLP/testLokalisasi.jpg> -dont_show -out <predictResult.txt>
    subprocess.run(["darknet", "detector", "test", variables.OBJ_DATA_PATH, variables.CFG_PATH, variables.YOLO_WEIGHT_PATH, "-ext_output", img_path, "-dont_show", "-out", variables.TXT_RESULT_PATH])

    # call utils get bounding-box coordinate
    bounding_data = bounding_box.getBoundingBox(variables.TXT_RESULT_PATH)
    bounding_box_id = []
    # save bounding box data for every object in image
    for obj_count in range(len(bounding_data)):
        # save collected bounding box to DB
        bounding_box_data = db.BoundingBox(
            img_input_id = img_id,
            yolo_confidence = bounding_data[obj_count][6],
            center_x = bounding_data[obj_count][2],
            center_y = bounding_data[obj_count][3],
            width = bounding_data[obj_count][4],
            height = bounding_data[obj_count][5]
            )
        
        with Session(db.engine) as session:
            session.add(bounding_box_data)
            session.commit()
            
            bounding_box_id.append(bounding_box_data.id)
            
            session.close()

    # return db bounding box id
    return {"bounding_box_id": bounding_box_id}

# extract plates from img_input
@router.post("/get-cropped-img/{bounding_box_id}")
async def get_cropped_img(bounding_box_id):
    return {"response":"200 OK"}

@router.get("/get-history/all")
async def read_all_history():
    return {"history_id": ['id_list_and_data']}

@router.get("/get-history/{inference_id}")
async def specific_history(inference_id: int):
    return {"history_id": inference_id}

@router.get('/get-image')
def get_all_image_path():
    query = select(tables.tbl_img_input)
    results = db.engine.execute(query).fetchall()
    payload = []
    for row in results:
        payload.append(row)
    return payload

@router.get('/get-one-image/{image_id}')
def get_image(image_id):
    query = select(tables.tbl_img_input).where(tables.tbl_img_input.c.id==image_id)
    result = db.engine.execute(query).fetchone()

    if not result:
        raise HTTPException(status_code=400, detail="File not found")
    
    file_location = "{}/{}".format(variables.INPUT_IMG_PATH, result[1])
    
    return responses.FileResponse(file_location)

@router.get('/get-multiple-image/{image_ids}')
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