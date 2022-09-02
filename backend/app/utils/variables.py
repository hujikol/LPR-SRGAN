import os

WORKSPACE = os.environ.get('WORKSPACE')

INPUT_IMG_PATH = "{}/image-dataset/highres-img".format(WORKSPACE)
CROP_IMG_PATH = "{}/image-dataset/cropped-img".format(WORKSPACE)
SUPER_IMG_PATH = "{}/image-dataset/super-result".format(WORKSPACE)

MODEL_PATH = "{}/model".format(WORKSPACE)
JSON_RESULT_PATH = "{}/json-result".format(WORKSPACE)