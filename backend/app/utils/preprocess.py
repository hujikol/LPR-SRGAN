import cv2
import numpy as np
import datetime
from PIL import Image

def open_img(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    return img

def load_img(img_path):
    img = Image.open(img_path)
    img = img.resize([64,32])
    img = np.array(img)
    return np.expand_dims(img, axis=0)

def save_img(folder_path, img_type, img, index = 0, pil=False):
    time = datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S:%f")
    
    # ex img_path = '/image-dataset/highres-img/img_highres_02-09-2022 09:43:07'
    img_path = "{}/img_{}_{}_{}.jpg".format(folder_path, img_type, index, time)

    if pil:
        img = Image.fromarray(img.numpy())
        img.save(img_path)
    else:
        cv2.imwrite(img_path, img)
    
    return img_path

# normalize img before SRGAN
def normalize_img(img):
    img_arr = np.array([img])
    img_arr = img_arr / 255.
    
    return img_arr

def normalize_img01(img_arr):
    return img_arr / 255.0
    
# normalize RGB images to [-1,1]
def normalize_img11(img_arr):
    return img_arr / 127.5

def denormalize_img(img_arr):
    img = img_arr * 255.
    
    return img[0,:,:,:]

def denormalize_img11(img_arr):
    return (img_arr + 1) * 127.5

def resize_img(img):
    img = cv2.resize(img,(64,32))
    
    return img

# img thresholding before easy ocr
def tresholding(img_path):
    img = open_img(img_path)
    
    # convert image to gray, 1 color channel
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    
    # convert image to binary
    _, thresh_otsu_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    return thresh_otsu_img