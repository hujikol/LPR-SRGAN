from keras.models import load_model
from utils import preprocess, variables

def get_super_img(img_path, img_index):
    generator = load_model(variables.MODEL_SRGAN_PATH, compile = False)
    
    # pre process img
    img = preprocess.open_img(img_path)
    img = preprocess.resize_img(img)
    img_arr = preprocess.normalize_img(img)
    
    super_img = generator.predict(img_arr)
    
    # get normal matriks range of 255 then save the image
    img = preprocess.denormalize_img(super_img)
    super_img_path = preprocess.save_img(variables.SUPER_IMG_PATH, "super", img, img_index)
    
    return super_img_path