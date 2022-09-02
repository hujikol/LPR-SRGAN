import os

WORKSPACE = os.environ.get('WORKSPACE')

INPUT_IMG_PATH = "{}/image-dataset/highres-img".format(WORKSPACE)
CROP_IMG_PATH = "{}/image-dataset/cropped-img".format(WORKSPACE)
SUPER_IMG_PATH = "{}/image-dataset/super-result".format(WORKSPACE)

# ditambahi sampe filenya nanti, tapi disimpen di /model
OBJ_DATA_PATH = "{}/model".format(WORKSPACE)
CFG_PATH = "{}/model".format(WORKSPACE)
YOLO_WEIGHT_PATH = "{}/model".format(WORKSPACE)

MODEL_SRGAN_PATH = "{}/model".format(WORKSPACE)
TXT_RESULT_PATH = "{}/json-result".format(WORKSPACE)