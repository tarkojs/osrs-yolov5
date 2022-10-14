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


while True:

    print(f"time elapsed: roughly {round((tot / 60), 1)} minutes")
    
    randroll = randint(34, 50)
    start_timecount = time.time()

    im = ImageGrab.grab()
    results = model(im)
    resultsdf = results.pandas().xyxy[0]

    try:
        for i in range(len(resultsdf.name)):
            if resultsdf.name[i] == "invfull":
                if resultsdf.confidence[i] >= 0.7:
                    print(f"inventory full --> confidence: {resultsdf.confidence[i]}, dropping logs")
                    misc.drop_logs()
                    misc.customsleep(2)
    except:
        print(f"inventory considered not full --> continuing")
        pass


    try: 
        mid_x = round((resultsdf.xmin[0] + resultsdf.xmax[0]) / 4)
        mid_y = round((resultsdf.ymin[0] + resultsdf.ymax[0]) / 4)
        rand = randint(-35, 35)
        rand_ = randint(-35, 35)
        coords_rand = (mid_x + rand, mid_y + rand_)
        print(f"moving to {coords_rand}, confidence --> {resultsdf.confidence[0]}")
        pya.moveTo(coords_rand)
        pya.click()
        tot_2 = 0
        sleep(randint(9, 12))
        while True:
            im = ImageGrab.grab()
            results = model(im)
            resultsdf = results.pandas().xyxy[0]
            act_start = len(resultsdf.name)
            print(act_start)
            while True:
                timer_start = time.time()
                im = ImageGrab.grab()
                results = model(im)
                resultsdf = results.pandas().xyxy[0]
                act_check = len(resultsdf.name)
                print(act_check)
                if tot_2 > randroll:
                    print(f"feeling stagnant (no action for {randroll} seconds --> breaking")
                    break
                if act_check - act_start >= abs(1) or act_start - act_check >= abs(1):
                    print(f"character considered not active: {act_start} =/= {act_check} - difference of 2")
                    sleep(uniform(0.15, 3.24))
                    break
                try:
                    for i in range(len(resultsdf.name)):
                        if resultsdf.name[i] == "invfull":
                            if resultsdf.confidence[i] >= 0.7:
                                print(f"inventory full --> confidence: {resultsdf.confidence[i]}, dropping logs")
                                misc.drop_logs()
                                misc.customsleep(2)
                                break
                except:
                    print(f"inventory considered not full --> continuing")
                    pass
                timer_end = time.time()
                tot_2 += (timer_end - timer_start)
                timer_end = 0
                timer_start = 0
            break
    except:
        print(f"unable to click on a tree - continuing")
        pass

    end_timecount = time.time()
    tot += (end_timecount - start_timecount)
    end_timecount = 0
    start_timecount = 0

# another implementation for taking screenshots - messes with the colors on OSX

"""
while True:
    with mss.mss() as sct:
        # Part of the screen to capture
        monitor = {"top": 0, "left": 0, "width": 1440, "height": 900}

        while "Screen capturing":
            last_time = time.time()

            # Get raw pixels from the screen, save it to a Numpy array
            img = numpy.array(sct.grab(monitor))
            #imgread = cv.imwrite("temptree", img)
            results = model(img)

            resultsdf = results.pandas().xyxy[0]
            print(resultsdf)
            


            #print(results.pandas().xyxy[0].confidence)
            #rint(f"confidence: {results.pandas().xyxy[0][4]}")
            #results.print()  # or .show(), .save(), .crop(), .pandas(), etc.

            #print("fps: {}".format(1 / (time.time() - last_time)))

            #cv.imshow("curr.haystack.png", img)

  # or file, Path, PIL, OpenCV, numpy, list

# Inference
results = model(img)

# Results
results.print()  # or .show(), .save(), .crop(), .pandas(), etc.
"""
