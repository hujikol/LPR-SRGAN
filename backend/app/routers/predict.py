from unittest import result
import aiofiles
import zipfile 
import subprocess
import os

from datetime import datetime, timezone
from sqlalchemy.orm import Session
from io import BytesIO
from fastapi import APIRouter, File, UploadFile, HTTPException, responses
from sqlalchemy import select
from db import db
from utils import variables, preprocess, bounding_box, crop_img

router = APIRouter()

timeNow = datetime.now().replace(tzinfo=timezone.utc).strftime("%d-%m-%Y %H:%M:%S")


@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.post("/upload-img")
async def upload_img(file: UploadFile = File(...)):
    if file.content_type != "image/jpeg":
        raise HTTPException(status_code=415, detail="Only support .jpg or .jpeg file")

    output_file = "{}/img_input_{}.jpg".format(variables.INPUT_IMG_PATH, timeNow)
    
    async with aiofiles.open(output_file, 'wb') as out_file:
        img_input_obj = db.ImgInput(img_path = output_file)
        with Session(db.engine) as session:
            # saving into ImgInput db
            session.add(img_input_obj)
            session.commit()
            
            img_id = img_input_obj.id
            
            # saving into History db
            history_obj = db.History(img_input_id = img_id)
            session.add(history_obj)
            session.commit()
            
            img_id = history_obj.img_input_id
            
            session.close()

        content = await file.read()
        await out_file.write(content)

    return {"id": img_id}

# get img bounding-box and save to db BoundingBox
@router.post("/get-bounding-box/{img_id}")
async def get_bounding_box(img_id):
    query = select(db.ImgInput).where(db.ImgInput.id == img_id)
    with Session(db.engine) as session:
        result = session.execute(query).fetchone()[0]
        img_path = result.img_path
        
        session.close()
    if not result:
        raise HTTPException(status_code = 400, detail = "Image id not found")
    
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
    return {"img_id": img_id}

# extract plates from img_input
@router.post("/get-cropped-img/{img_id}")
async def get_cropped_img(img_id):
    queryImg = select(db.ImgInput).where(db.ImgInput.id == img_id)
    queryBBox = select(db.BoundingBox).where(db.BoundingBox.img_input_id == img_id)
    queryHistory = select(db.History).where(db.History.img_input_id == img_id)
    
    with Session(db.engine) as session:
        # get ImgInput path
        result = session.execute(queryImg).fetchone()[0]
        resultBBox = session.execute(queryBBox).fetchall()
        img_path = result.img_path
        img_index = 0
        # cropping all bbox predicted from the ImgInput
        for row in resultBBox:
            cropped_img_path = crop_img.get_cropped_img(
                img_path, 
                row.BoundingBox.center_x,
                row.BoundingBox.center_y,
                row.BoundingBox.width,
                row.BoundingBox.height,
                img_index
                )
            img_index += 1
            
            # saving each cropped img to CroppedImg db
            cropped_img_obj = db.CroppedImg(img_path = cropped_img_path)
            session.add(cropped_img_obj)
            session.commit()
            cropped_img_id = cropped_img_obj.id
            
            # get History id of current ImgInput
            result = session.execute(queryHistory).fetchone()[0]
            history_id = result.id
            
            # save history id and cropped img id to CroppedAndSuper tbl
            cropped_super_obj = db.CroppedAndSuper(
                history_id = history_id,
                cropped_img_id = cropped_img_id
                )
            session.add(cropped_super_obj)
            session.commit()
                
    session.close()
    
    return {"historyId" : history_id}

@router.get("/get-history/all")
async def read_all_history():
    return {"history_id": ['id_list_and_data']}

@router.get("/get-history/{inference_id}")
async def specific_history(inference_id: int):
    return {"history_id": inference_id}

@router.get('/get-image')
def get_all_image_path():
    query = select(db.ImgInput)
    results = db.engine.execute(query).fetchall()
    payload = []
    for row in results:
        payload.append(row)
    return payload

@router.get('/get-one-image/{image_id}')
def get_image(image_id):
    query = select(db.ImgInput).where(db.ImgInput.id == image_id)
    result = db.engine.execute(query).fetchone()

    if not result:
        raise HTTPException(status_code=400, detail="File not found")
    
    file_location = "{}/{}".format(variables.INPUT_IMG_PATH, result[1])
    
    return responses.FileResponse(file_location)

@router.get('/get-multiple-image/{image_ids}')
def get_zip_image(image_ids):    
    ids = tuple(map(int, image_ids.split(",")))
    query = select(db.ImgInput).filter(db.ImgInput.id.in_(ids))
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