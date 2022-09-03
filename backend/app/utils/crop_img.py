import cv2
import preprocess
import variables

def yoloLine2Shape(imgHeight, imgWidth, xcen, ycen, w, h):
    xmin = float(xcen) - float(w) / 2
    xmax = float(xcen) + float(w) / 2
    ymin = float(ycen) - float(h) / 2
    ymax = float(ycen) + float(h) / 2
    
    # calculating the real pixel coordinate
    xmin = int(imgWidth * xmin)
    xmax = int(imgWidth * xmax)
    ymin = int(imgHeight * ymin)
    ymax = int(imgHeight * ymax)

    return xmin, ymin, xmax, ymax

def get_cropped_img(origin_img_path, x_relative, y_relative, w_relative, h_relative):
    img = cv2.imread(origin_img_path)

    # get image size
    imgHeight, imgWidth, _ = img.shape

    # get coordinate
    xmin, ymin, xmax, ymax = yoloLine2Shape(imgHeight, imgWidth, x_relative, y_relative, w_relative, h_relative)
    
    crop_img = img[ymin:ymax,xmin:xmax]
    cropped_img_path = preprocess.save_img(variables.CROP_IMG_PATH, "cropped", crop_img)
    
    return cropped_img_path