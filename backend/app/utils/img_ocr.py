import easyocr
from utils import preprocess, variables

reader = easyocr.Reader(['en'], gpu = False, download_enabled = False, model_storage_directory = variables.EASYOCR_MODEL_PATH)

def get_image_character(img_path, detail = 0):
    
    # extracting character from image without otsu preprocessing
    img_wo = preprocess.open_img(img_path)
    wo_pre_img_char = reader.readtext(img_wo, detail = detail)
    wo_pre_img_char = " ".join(wo_pre_img_char)
    
    # extracting character from otsu preprocessing
    img_otsu = preprocess.tresholding(img_path)
    otsu_img_char = reader.readtext(img_otsu, detail = detail)
    otsu_img_char = " ".join(otsu_img_char)
    
    return otsu_img_char, wo_pre_img_char