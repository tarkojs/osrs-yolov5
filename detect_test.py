import cv2 as cv
import time
import misc
import torch
import pandas as pd
import pyautogui as pya
from time import sleep
from random import randint, uniform
from PIL import ImageGrab


model = torch.hub.load('ultralytics/yolov5', 'custom', '/Users/tarkojuss/Desktop/vskoodkood/OSTreeDetection/yolov5/runs/train/exp13/weights/best.pt') 
model.conf = 0.7  # NMS confidence threshold
iou = 0.45  # NMS IoU threshold
agnostic = False  # NMS class-agnostic
multi_label = False  # NMS multiple labels per box
classes = None  # (optional list) filter by class, i.e. = [0, 15, 16] for COCO persons, cats and dogs
max_det = 10  # maximum number of detections per image
amp = False  # Automatic Mixed Precision (AMP) inference -- FALSE DEFAULT
tot = 0


def check_activity():
    while True:
        act_start = len(resultsdf.name)
        sleep(randint(3, 10))
        act_check = len(resultsdf)
        if act_start != act_check:
            break

while True:
    im = ImageGrab.grab()
    results = model(im)
    resultsdf = results.pandas().xyxy[0]

    print(len(resultsdf.name))


    



    