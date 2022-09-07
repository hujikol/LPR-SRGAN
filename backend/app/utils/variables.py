import os

WORKSPACE = os.environ.get('WORKSPACE')

INPUT_IMG_PATH = "{}/image-dataset/highres-img".format(WORKSPACE)
CROP_IMG_PATH = "{}/image-dataset/cropped-img".format(WORKSPACE)
SUPER_IMG_PATH = "{}/image-dataset/super-result".format(WORKSPACE)

OBJ_DATA_PATH = "{}/model/obj.data".format(WORKSPACE)
CFG_PATH = "{}/model/yolov4-obj.cfg".format(WORKSPACE)
YOLO_WEIGHT_PATH = "{}/model/yolov4-obj_last.weights".format(WORKSPACE)

MODEL_SRGAN_PATH = "{}/model/gen_SRGAN_60.h5".format(WORKSPACE)
TXT_RESULT_PATH = "{}/json-result/result.txt".format(WORKSPACE)
IMG_RESULT_PATH ="{}/predictions.jpg".format(WORKSPACE)

MODEL_PATH = "{}/model".format(WORKSPACE)
JSON_RESULT_PATH = "{}/json-result".format(WORKSPACE)