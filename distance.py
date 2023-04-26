import numpy as np
import cv2
import json
import cv2
import matplotlib
import matplotlib.pyplot as plt
import keras.utils as image
from numpy import cov
from numpy import trace
from numpy import iscomplexobj
from numpy.random import random
from scipy.linalg import sqrtm
from Levenshtein import distance as levenshtein_distance


# https://gist.github.com/bowenc0221/71f7a02afee92646ca05efeeb14d687d
# General util function to get the boundary of a binary mask.
def mask_to_boundary(mask, dilation_ratio=0.02):
    """
    Convert binary mask to boundary mask.
    :param mask (numpy array, uint8): binary mask
    :param dilation_ratio (float): ratio to calculate dilation = dilation_ratio * image_diagonal
    :return: boundary mask (numpy array)
    """
    h, w = mask.shape
    img_diag = np.sqrt(h ** 2 + w ** 2)
    dilation = int(round(dilation_ratio * img_diag))
    if dilation < 1:
        dilation = 1
    # Pad image so mask truncated by the image border is also considered as boundary.
    new_mask = cv2.copyMakeBorder(mask, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0)
    kernel = np.ones((3, 3), dtype=np.uint8)
    new_mask_erode = cv2.erode(new_mask, kernel, iterations=dilation)
    mask_erode = new_mask_erode[1 : h + 1, 1 : w + 1]
    # G_d intersects G in the paper.
    return mask - mask_erode


def boundary_iou(gt, dt, dilation_ratio=0.02):
    """
    Compute boundary iou between two binary masks.
    :param gt (numpy array, uint8): binary mask
    :param dt (numpy array, uint8): binary mask
    :param dilation_ratio (float): ratio to calculate dilation = dilation_ratio * image_diagonal
    :return: boundary iou (float)
    """
    gt_boundary = mask_to_boundary(gt, dilation_ratio)
    dt_boundary = mask_to_boundary(dt, dilation_ratio)
    intersection = ((gt_boundary * dt_boundary) > 0).sum()
    union = ((gt_boundary + dt_boundary) > 0).sum()
    boundary_iou = intersection / union
    return boundary_iou

def get_distance_metrics(json_file, masked_image, valid_lps):
    simulator_img=image.load_img(masked_image, target_size=(2048,2048),color_mode="grayscale"); #loading image and then convert it into grayscale and with it's target size 
    simulator_img=image.img_to_array(simulator_img); #convert image into array
    lev = 20
    box_score = ocr_score = 0
    ocr_text = "XXXXXX"
    iou = fid = 10000
    with open(json_file, 'r') as file_name:
        json_content = json.load(file_name)
        # print(json_content)
        points = []
        for object in json_content['result']['localizedObjectAnnotations']:
            points.append(object['points'])
            ocr_text = object['attributes']['ocr'][0]
            ocr_score = object['attributes']['ocr'][1]
            box_score = object['score']
            print('CAMEA Detected License Plate:  ' + ocr_text   +  " Score:" + str(ocr_score) )

            ocr_img = np.zeros([2048, 2048],dtype=np.uint8)
            pts = np.array(object['points'], np.int32)
            cv2.fillPoly(ocr_img, [pts], 255)
            cv2.imshow('Simulator', simulator_img)
            cv2.waitKey(1000)
            cv2.imshow('LP detector', ocr_img)
            cv2.waitKey(1000)

            #print(points)
            #print("SIM", ocr_img.shape)
            #print("OCR", simulator_img.shape)
            simulator_img= np.squeeze(simulator_img)  # Remove axes of length one
            #print("OCR*", simulator_img.shape)
            iou = boundary_iou(simulator_img, ocr_img )
            
            for lp in valid_lps:
                lev = min(lev, levenshtein_distance(lp, object['attributes']['ocr'][0]))
    result = {
        "iou" : iou,
        "lev" : lev,
        "box_score" : box_score,
        "ocr_score" : ocr_score}
    print("Distances:", result)
    return result


if __name__ == "__main__":
    get_distance_metrics('test-files/ocr.json', 'test-files/sim.png', ['AAAAA', 'BBBBB'])