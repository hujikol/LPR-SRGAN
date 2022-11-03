import tensorflow as tf
from model import srresnet
from utils import preprocess, variables

def get_super_img(img_path, img_index):
    # building model and load saved weights
    model = srresnet.build_srresnet()
    model.load_weights(variables.SRGAN_WEIGHTS_PATH)
    
    # load image
    img = preprocess.load_img(img_path)
    
    # generate SR images
    sr = model.predict(img)[0]
    
    # save the image
    super_img_path = preprocess.save_img(variables.SUPER_IMG_PATH, "super", sr, img_index)
    
    return super_img_path