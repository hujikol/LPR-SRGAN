import aiofiles
import subprocess
import os
import shutil
import base64

from unittest import async_case, result
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from io import BytesIO
from fastapi import APIRouter, File, UploadFile, HTTPException, responses
from sqlalchemy import select, update, delete
from db import db
from utils import variables, super_img, new_super_img, bounding_box, crop_img, img_ocr

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.post("/upload-img")
async def upload_img(file: UploadFile = File(...)):
    if file.content_type != "image/jpeg":
        raise HTTPException(status_code=415, detail="Only support .jpg or .jpeg file")

    timeNow = datetime.now().replace(tzinfo=timezone.utc).strftime("%d-%m-%Y %H:%M:%S:%f")
    base_file_name = "img_input_{}.jpg".format(timeNow)
    output_file = "{}/{}".format(variables.INPUT_IMG_PATH, base_file_name)
    
    async with aiofiles.open(output_file, 'xb') as out_file:
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
        out_file.close()
        
    session.close()
    return {"id": img_id}

# get img bounding-box and save to db BoundingBox
@router.post("/get-bounding-box/{img_id}")
async def get_bounding_box(img_id):
    query = select(db.ImgInput).where(db.ImgInput.id == img_id)
    with Session(db.engine) as session:
        # get img input path
        result = session.execute(query).fetchone()[0]
        img_path = result.img_path
        
        session.close()
    if not result:
        raise HTTPException(status_code = 400, detail = "Image id not found")
    
    # call darknet to run yolov4
    # !./darknet detector test <LPR/obj.data> <LPR/darknet/yolov4-obj.cfg> <LPR/detectionBKP/yolov4-obj_last.weights> -ext_output <LPR/testingLP/testLokalisasi.jpg> -dont_show -out <predictResult.txt>
    subprocess.run(["darknet", "detector", "test", variables.OBJ_DATA_PATH, variables.CFG_PATH, variables.YOLO_WEIGHT_PATH, "-ext_output", img_path, "-dont_show", "-out", variables.TXT_RESULT_PATH])

    # copy img prediction w/ bbox into highres-image folder
    shutil.copy(variables.IMG_RESULT_PATH, img_path.replace(".", "_wbbox."))
    
    # call utils get bounding-box coordinate
    bounding_data = bounding_box.getBoundingBox(variables.TXT_RESULT_PATH)
    
    # if no bounding data were found, retunring -1 for error
    if len(bounding_data) == 0:
        return {"img_id":-1}
    
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

# Generating Super Images
@router.post("/super-img/{history_id}")
async def get_super_resolution_img(history_id):
    # get all CroppedAndSuper id for current history id
    queryCnS = select(db.CroppedAndSuper).where(db.CroppedAndSuper.history_id == history_id)
    
    with Session(db.engine) as session:
        #  get all CroppedAndSuper data for current history id
        resultCnS = session.execute(queryCnS).fetchall()

        img_index = 0
        # for all cropped img create super resolution img
        for row in resultCnS:
            
            # get cropped img path
            queryCropImg = (
                select(db.CroppedImg)
                .where(db.CroppedImg.id == row.CroppedAndSuper.cropped_img_id)
                )
            cropImg = session.execute(queryCropImg).fetchone()
            croppedImg_path = cropImg[0].img_path
            
            # get super resolution img path
            # super_img_path = super_img.get_super_img(croppedImg_path, img_index)
            super_img_path = new_super_img.get_super_img(croppedImg_path, img_index)
            
            img_index += 1
            
            # saving each super img to SuperImg db
            super_img_obj = db.SuperImg(img_path = super_img_path)
            session.add(super_img_obj)
            session.commit()
            super_img_id = super_img_obj.id
            
            # save super img id to CroppedAndSuper tbl based on CroppedAndSuper id
            updateCnS = (
                update(db.CroppedAndSuper)
                .where(db.CroppedAndSuper.id == row.CroppedAndSuper.id)
                .values(super_img_id = super_img_id)
                )
            session.execute(updateCnS)
            session.commit()
                
    session.close()
    return {"historyId" : history_id}

@router.post("/easy-ocr/{history_id}")
async def get_img_character(history_id):
    # get all CroppedAndSuper data for current history id
    queryCnS = select(db.CroppedAndSuper).where(db.CroppedAndSuper.history_id == history_id)

    with Session(db.engine) as session:
    # get all CroppedAndSuper data for current history id
        resultCnS = session.execute(queryCnS).fetchall()
        
        # for all cropped and super img create super resolution img
        for row in resultCnS:
            # get cropped img path
            queryCropImg = (
                select(db.CroppedImg)
                .where(db.CroppedImg.id == row.CroppedAndSuper.cropped_img_id))
            cropImg = session.execute(queryCropImg).fetchone()
            croppedImg_path = cropImg[0].img_path
            
            # extracting character from cropped img
            croppedImg_char, croppedImg_wo_char = img_ocr.get_image_character(croppedImg_path)
            
            # get super resolution img path
            querySuperImg = (
                select(db.SuperImg)
                .where(db.SuperImg.id == row.CroppedAndSuper.super_img_id))
            superImg = session.execute(querySuperImg).fetchone()
            superImg_path = superImg[0].img_path
            
            # extracting character from super img
            superImg_char, superImg_wo_char = img_ocr.get_image_character(superImg_path)
            
            # saving into CroppedAndSuper
            updateCnS = (
                update(db.CroppedAndSuper)
                .where(db.CroppedAndSuper.id == row.CroppedAndSuper.id)
                .values(
                    cropped_text = croppedImg_char,
                    cropped_wo_text = croppedImg_wo_char,
                    super_text = superImg_char,
                    super_wo_text = superImg_wo_char
                    )
                )
            session.execute(updateCnS)
            session.commit()
            
        session.close()    
    return {"historyId": history_id}

@router.get("/get-history/all")
async def read_all_history():
    queryHistory = select(db.History)
    historyData = []
    with Session(db.engine) as session:
        resultHistory = session.execute(queryHistory).fetchall()
        
        for row in resultHistory:
            # get img input in byte64
            queryImgId = select(db.History.img_input_id).where(db.History.id == row.History.img_input_id)
            img_id = session.execute(queryImgId).fetchone()
            
            queryImgPath = (
                select(db.ImgInput.img_path)
                .where(db.ImgInput.id == img_id[0]))
            img_path = session.execute(queryImgPath).fetchone()
            img_path = img_path[0].replace(".", "_wbbox.")
            with open(img_path, 'rb') as f:
                inputImg_byte = base64.b64encode(f.read())
            
            # counting detected plates
            queryBBCount = (select(db.BoundingBox).where(db.BoundingBox.img_input_id == img_id[0]))
            resultBBCount = session.execute(queryBBCount).fetchall()
            bboxCount = len(resultBBCount)
            
            # get infference date time
            dateTime = row.History.date_time.strftime("%d-%m-%Y %H:%M:%S")
                                      
            historyData.append({
                "historyId" : row.History.id,
                "inputImg_byte" : inputImg_byte,
                "dateTime" : dateTime,
                "bboxCount" : bboxCount,
            })
            
    session.close()
    if len(historyData) == 0:
        return {"historyData" : 0}
    return {"historyData": historyData}

@router.post("/get-history/{history_id}")
async def specific_history(history_id):
    cns_data = []
    
    # select img input path
    queryImgId = select(db.History.img_input_id).where(db.History.id == history_id)
    # select cropped img and super img path where id history
    queryCnS = select(db.CroppedAndSuper).where(db.CroppedAndSuper.history_id == history_id)
    with Session(db.engine) as session:
        # get img input id
        img_id = session.execute(queryImgId).fetchone()
        
        # get yolo avg confidence from all bbox in image
        queryYoloConf = select(db.BoundingBox.yolo_confidence).where(db.BoundingBox.img_input_id == img_id[0])
        yoloConf = session.execute(queryYoloConf).fetchall()
        yoloConf = [item for item, in yoloConf]
        avgYoloConf = sum(yoloConf) / len(yoloConf)
        
        # get img input in byte64
        queryImgPath = select(db.ImgInput.img_path).where(db.ImgInput.id == img_id[0])
        img_path = session.execute(queryImgPath).fetchone()
        img_path = img_path[0].replace(".", "_wbbox.")
        with open(img_path, 'rb') as f:
            yolo_img_byte = base64.b64encode(f.read())
        
        # get all Cropped and Super resolution image and text from one image input
        resultCnS = session.execute(queryCnS).fetchall()
        for row in resultCnS:
            # get cropped img byte64 data
            queryCropImg = (
                select(db.CroppedImg)
                .where(db.CroppedImg.id == row.CroppedAndSuper.cropped_img_id))
            cropImg = session.execute(queryCropImg).fetchone()
            croppedImg_path = cropImg[0].img_path
            with open(croppedImg_path, 'rb') as f:
                cropped_img_byte = base64.b64encode(f.read())
            
            # get cropped img size in KB
            crop_img_size = os.stat(croppedImg_path).st_size / 1024
            
            # get super resolution img byte64 data
            querySuperImg = (
                select(db.SuperImg)
                .where(db.SuperImg.id == row.CroppedAndSuper.super_img_id))
            superImg = session.execute(querySuperImg).fetchone()
            superImg_path = superImg[0].img_path
            with open(superImg_path, 'rb') as f:
                super_img_byte = base64.b64encode(f.read())

            # get super img size in KB
            super_img_size = os.stat(superImg_path).st_size / 1024
            
            # get character
            crop_text = row.CroppedAndSuper.cropped_text
            crop_wo_text = row.CroppedAndSuper.cropped_wo_text
            super_text = row.CroppedAndSuper.super_text
            super_wo_text = row.CroppedAndSuper.super_wo_text
            
            # append to cns data
            cns_data.append({
                "crop_img_byte" : cropped_img_byte,
                "crop_img_size" : crop_img_size,
                "crop_text" : crop_text,
                "crop_wo_text" : crop_wo_text,
                "super_img_byte" : super_img_byte,
                "super_img_size" : super_img_size,
                "super_text" : super_text,
                "super_wo_text" : super_wo_text,
            })
    
    session.close()
    # return cropped + super img + text, (w&wo otsu), get yolo confidence
    return {
        "yolo_confidence" : avgYoloConf,
        "yolo_img_byte" : yolo_img_byte,
        "cns_data" : cns_data,
    }

# delete multiple or single specified history by id
@router.post("/delete/{history_id}")
async def delete_specific_history(history_id):
    # parsing list of history_id
    id_list = history_id.split(",")
    res = []
    
    with Session(db.engine) as session:
        # for every id
        for index, hId in enumerate(id_list):
            # get img_input id
            queryImgId = select(db.History.img_input_id).where(db.History.id == hId)
            img_id = session.execute(queryImgId).scalars().one_or_none()
            
            # select img input file path
            querryImgInputPath = select(db.ImgInput.img_path).where(db.ImgInput.id == img_id)
            imgInputPath = session.execute(querryImgInputPath).scalars().one_or_none()
            
            # get bounding-box id
            queryBboxId = select(db.BoundingBox.id).where(db.BoundingBox.img_input_id == img_id)
            bboxIdList = session.execute(queryBboxId).scalars().all()
            bboxRes = []
            
            # delete for every bounding-box
            for bboxId in bboxIdList:
                # delete bounding box
                if session.execute(select(db.BoundingBox).where(db.BoundingBox.id == bboxId)).one_or_none() != None:
                    delBbox = delete(db.BoundingBox).where(db.BoundingBox.id == bboxId)
                    delBboxRes = session.execute(delBbox)
                    bboxRes.append(delBboxRes)
                
            # get cropped & super id
            queryCnS = select(db.CroppedAndSuper).where(db.CroppedAndSuper.history_id == history_id)
            resultCnS = session.execute(queryCnS).scalars().all()

            cnsRes = cropRes = superRes = []

            # delete for every cropped and super image within img_input
            for cnsImg in resultCnS:
                # get cropped img file name
                queryCropFileName = select(db.CroppedImg.img_path).where(db.CroppedImg.id == cnsImg.cropped_img_id)
                cropFileName = session.execute(queryCropFileName).scalars().one_or_none()
                
                # delete cropped img
                if cropFileName != None:
                    if os.path.exists(cropFileName):
                        os.remove(cropFileName)
                        
                if session.execute(select(db.CroppedImg).where(db.CroppedImg.id == cnsImg.cropped_img_id)).one_or_none() != None:
                    delCropped = delete(db.CroppedImg).where(db.CroppedImg.id == cnsImg.cropped_img_id)
                    delCroppedRes = session.execute(delCropped)
                    cropRes.append(delCroppedRes)
                    
                # get super_img id
                querySuperFileName = select(db.SuperImg.img_path).where(db.SuperImg.id == cnsImg.super_img_id)
                superFileName = session.execute(querySuperFileName).scalars().one_or_none()
                
                # delete super_img
                if superFileName != None:
                    if os.path.exists(superFileName):
                        os.remove(superFileName)
                
                if session.execute(select(db.SuperImg).where(db.SuperImg.id == cnsImg.super_img_id)).one_or_none() != None:
                    delSuper = delete(db.SuperImg).where(db.SuperImg.id == cnsImg.super_img_id)
                    delSuperRes = session.execute(delSuper)
                    superRes.append(delSuperRes)
                
                
                # delete CnS row
                if session.execute(select(db.CroppedAndSuper).where(db.CroppedAndSuper.history_id == history_id)).first() != None:
                    delCns = delete(db.CroppedAndSuper).where(db.CroppedAndSuper.history_id == history_id)
                    delCnsRes = session.execute(delCns)
                    cnsRes.append(delCnsRes)
                
            # delete img_input files
            if imgInputPath != None:
                if os.path.exists(imgInputPath):
                    os.remove(imgInputPath)
                    
                # delete img with bbox
                if os.path.exists(imgInputPath.replace(".", "_wbbox.")):
                    os.remove(imgInputPath.replace(".", "_wbbox."))
            
            # delete history
            if session.execute(select(db.History).where(db.History.id == hId)).one_or_none() != None:
                delHistory = delete(db.History).where(db.History.id == hId)
                historyRes = session.execute(delHistory)
            
            res.append(
                {
                    "delHistory": historyRes,
                    "delBBox": bboxRes,
                    "delCnS": cnsRes,
                    "delCrop": cropRes,
                    "delSuper": superRes,
                }
            )
            session.commit()
        
        session.close()
    return res
