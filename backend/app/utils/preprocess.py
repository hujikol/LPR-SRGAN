import cv2
import numpy as np
import datetime

def open_img(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    return img

def save_img(folder_path, img_type, img, index = 0):
    time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    
    # ex img_path = '/image-dataset/highres-img/img_highres_02-09-2022 09:43:07'
    img_path = "{}/img_{}_{}_{}.jpg".format(folder_path, img_type, index, time)

    cv2.imwrite(img_path, img)
    
    return img_path

# normalize img before SRGAN
def normalize_img(img):
    img_arr = np.array([img])
    img_arr = img_arr / 255.
    
    return img_arr

# img thresholding before easy ocr
def tresholding(img_path):
    img = open_img(img_path)
    
    # convert image to gray, 1 color channel
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    
    # convert image to binary
    _, thresh_otsu_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    return thresh_otsu_img