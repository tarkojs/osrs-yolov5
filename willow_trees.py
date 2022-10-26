import time
import misc
import torch
import pyautogui as pya
from time import sleep
from random import randint, uniform
from PIL import ImageGrab

# ideas --> clean the code, add automatic log-on, create & train a better model, 

model = torch.hub.load('ultralytics/yolov5', 'custom', '/Users/tarkojuss/Desktop/vskoodkood/OSTreeDetection/model_weights/weights/best.pt')
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
    
    randroll = randint(30, 60)
    start_timecount = time.time()

    im = ImageGrab.grab()
    results = model(im)
    resultsdf = results.pandas().xyxy[0]

    try:
        for i in range(len(resultsdf.name)):
            if resultsdf.name[i] == "invfull":
                if resultsdf.confidence[i] >= 0.7:
                    print(f"inventory full --> confidence: {round(resultsdf.confidence[i], 2)}, dropping logs")
                    misc.drop_logs()
                    misc.customsleep(2)
    except:
        print(f"inventory considered not full --> continuing")
        pass


    try: 
        mid_x = round((resultsdf.xmin[0] + resultsdf.xmax[0]) / 4) # divided by 2 to get the centers of the boxes
        mid_y = round((resultsdf.ymin[0] + resultsdf.ymax[0]) / 4) # divided by 2 again due to the screenshots being 2880x1800, the actual res is 1440x900
        rand = randint(-35, 35)
        rand_ = randint(-35, 35)
        coords_rand = (mid_x + rand, mid_y + rand_)
        print(f"moving to & clicking {coords_rand}, confidence --> {round(resultsdf.confidence[0], 2)}")
        pya.moveTo(coords_rand)
        pya.click()
        tot_2 = 0
        det_sleep = uniform(7, 9)
        print(f"waiting before detecting further --> sleeping for {round(det_sleep, 2)} seconds")
        sleep(det_sleep)
        while True:
            im = ImageGrab.grab()
            results = model(im)
            resultsdf = results.pandas().xyxy[0]
            act_start = len(resultsdf.name)
            print(f"initial number of detections: {act_start}")
            while True:
                timer_start = time.time()
                im = ImageGrab.grab()
                results = model(im)
                resultsdf = results.pandas().xyxy[0]
                act_check = len(resultsdf.name)
                print(f"current number of detections: {act_check}")
                if tot_2 > randroll:
                    print(f"feeling stagnant (no action for {randroll} seconds) --> continuing")
                    break
                if act_check - act_start >= abs(1) or act_start - act_check >= abs(1):
                    print(f"character considered inactive due to a difference in detection: {act_start} =/= {act_check}")
                    det_sleep = uniform(0.15, 6.24)
                    print(f"waiting before detecting --> sleeping for {round(det_sleep, 2)} seconds")
                    sleep(det_sleep)
                    break
                try:
                    for i in range(len(resultsdf.name)):
                        if resultsdf.name[i] == "invfull":
                            if resultsdf.confidence[i] >= 0.7:
                                print(f"inventory full --> confidence: {round(resultsdf.confidence[i], 2)}, dropping logs")
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
        print(f"unable to click on a tree --> continuing")
        pass

    end_timecount = time.time()
    tot += (end_timecount - start_timecount)
    end_timecount = 0
    start_timecount = 0

# another implementation for taking screenshots

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
