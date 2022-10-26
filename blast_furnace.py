import misc
import torch
import pyautogui as pya
from time import sleep
from random import randint, uniform
from PIL import ImageGrab

"""
bank screen --> fill coal bag, take coal, close bank
pt2 --> click on belt, wait, empty coal bag, click on belt
pt3 --> go to bank, fill coal bag, take ores, close bank
pt4 --> click on belt, wait, take bars coords if possible
pt5 --> click on bars, click space/continue, click on bank
pt6 --> deposit all but the coal bag, the loop goes again
"""

model = torch.hub.load('ultralytics/yolov5', 'custom', '/Users/tarkojuss/Desktop/vskoodkood/OSTreeDetection/yolov5/runs/train/exp20/weights/best.pt') 
model.conf = 0.3  # NMS confidence threshold
iou = 0.45  # NMS IoU threshold
agnostic = False  # NMS class-agnostic
multi_label = False  # NMS multiple labels per box
classes = None  # (optional list) filter by class, i.e. = [0, 15, 16] for COCO persons, cats and dogs
max_det = 10  # maximum number of detections per image
amp = False  # Automatic Mixed Precision (AMP) inference -- FALSE DEFAULT

def randomized_bank_click(tuple):
    x = tuple[0]
    y = tuple[1]
    rand = randint(-9, 9)
    rand_ = randint(-9, 9)
    coords_rand = (x + rand, y + rand_)
    print(f"moving to & clicking {coords_rand}")
    pya.moveTo(coords_rand)
    pya.click()
    det_sleep = uniform(0, 3)
    print(f"waiting before detecting further --> sleeping for {round(det_sleep, 2)} seconds")
    sleep(det_sleep)

def randomized_click(tuple):
    x = tuple[0]
    y = tuple[1]
    rand = randint(-5, 5)
    rand_ = randint(-5, 5)
    coords_rand = (x + rand, y + rand_)
    print(f"moving to & clicking {coords_rand}")
    pya.moveTo(coords_rand)
    pya.click()
    det_sleep = uniform(0, 1.2)
    print(f"waiting before detecting further --> sleeping for {round(det_sleep, 2)} seconds")
    sleep(det_sleep)

def randomized_click_bank(tuple):
    x = tuple[0]
    y = tuple[1]
    rand = randint(-3, 3)
    rand_ = randint(-3, 3)
    coords_rand = (x + rand, y + rand_)
    print(f"moving to & clicking {coords_rand}")
    pya.moveTo(coords_rand)
    pya.click()
    det_sleep = uniform(0, 1.2)
    print(f"waiting before detecting further --> sleeping for {round(det_sleep, 2)} seconds")
    sleep(det_sleep)

def banking_first():
    randomized_bank_click((897, 281))
    sleep(uniform(0.3, 1.3))
    randomized_bank_click((744, 184))
    sleep(uniform(0.15, 0.6))
    pya.press("esc")

def banking_second():
    randomized_bank_click((899, 283))
    sleep(uniform(0.3, 1.35))
    randomized_bank_click((744, 148))
    sleep(uniform(0.25, 1.3))
    pya.press("esc")

def first_trip():
    im = ImageGrab.grab()
    results = model(im)
    resultsdf = results.pandas().xyxy[0]
    try:
        for i in range(len(resultsdf.name)):
            if resultsdf.name[i] == "belt":
                if resultsdf.confidence[i] >= 0.5:
                    mid_x = round((resultsdf.xmin[i] + resultsdf.xmax[i]) / 4)
                    mid_y = round((resultsdf.ymin[i] + resultsdf.ymax[i]) / 4)
                    if mid_x < 833 and mid_x > 317:
                        print(f"({mid_x}, {mid_y}) --> coords within vision --> clicking")
                        print(f"going to belt --> confidence: {round(resultsdf.confidence[i], 2)}")
                        randomized_click((mid_x, mid_y))
                        sleep(uniform(12, 21))

                        pya.moveTo((897 + randint(-3, 3), 281 + randint(-3, 3)))
                        misc.drop()

                        im = ImageGrab.grab()
                        results = model(im)
                        resultsdf = results.pandas().xyxy[0]

                        for i in range(len(resultsdf.name)):
                            if resultsdf.name[i] == "belt":
                                if resultsdf.confidence[i] >= 0.5:
                                    mid_x = round((resultsdf.xmin[i] + resultsdf.xmax[i]) / 4)
                                    mid_y = round((resultsdf.ymin[i] + resultsdf.ymax[i]) / 4)
                                    if mid_x < 833 and mid_x > 317:
                                        print(f"({mid_x}, {mid_y}) --> coords within vision --> clicking")
                                        print(f"going to belt --> confidence: {round(resultsdf.confidence[i], 2)}")
                                        randomized_click((mid_x, mid_y))
                                        sleep(uniform(11, 16))
                                        break
                        break

        for i in range(len(resultsdf.name)):
            if resultsdf.name[i] == "bank":
                mid_x = round((resultsdf.xmin[i] + resultsdf.xmax[i]) / 4)
                mid_y = round((resultsdf.ymin[i] + resultsdf.ymax[i]) / 4)
                if mid_x < 833 and mid_x > 317:
                    print(f"({mid_x}, {mid_y}) --> coords within vision --> clicking on bank")
                    randomized_click_bank((mid_x, mid_y))
                    sleep(uniform(13, 18))
                    break
    except:
        print(f"belt not seen --> continuing")
        pass


def second_trip():
    im = ImageGrab.grab()
    results = model(im)
    resultsdf = results.pandas().xyxy[0]
    try:
        for i in range(len(resultsdf.name)):
            if resultsdf.name[i] == "belt":
                if resultsdf.confidence[i] >= 0.5:
                    mid_x = round((resultsdf.xmin[i] + resultsdf.xmax[i]) / 4)
                    mid_y = round((resultsdf.ymin[i] + resultsdf.ymax[i]) / 4)
                    if mid_x < 833 and mid_x > 317:
                        print(f"({mid_x}, {mid_y}) --> coords within vision --> clicking")
                        print(f"going to belt --> confidence: {round(resultsdf.confidence[i], 2)}")
                        randomized_click((mid_x, mid_y))
                        sleep(uniform(7, 13))

                        pya.moveTo((897 + randint(-5, 5), 281 + randint(-5, 5)))
                        misc.drop()

                        sleep(uniform(0.3, 0.8))
                        pya.moveTo(590 + randint(-3, 3), 213 + randint(-3, 3))
                        pya.click()
                        break

        sleep(uniform(8, 15))

        im = ImageGrab.grab()
        results = model(im)
        resultsdf = results.pandas().xyxy[0]

        for i in range(len(resultsdf.name)):
            if resultsdf.name[i] == "belt":
                mid_x = round((resultsdf.xmin[i] + resultsdf.xmax[i]) / 4)
                mid_y = round((resultsdf.ymin[i] + resultsdf.ymax[i]) / 4)
                if mid_y > 235 and mid_x > 317 and mid_x < 835:
                    print(f"({mid_x}, {mid_y}) --> coords within vision --> got new coords for bars")
                    rand = randint(-5, 5)
                    rand_ = randint(-5, 5)
                    bars_coords_rand = (mid_x + rand, mid_y + rand_)
                    randomized_click_bank(bars_coords_rand)
                    sleep(uniform(4.5, 6))
                    pya.press("space")
                    sleep(uniform(0.3, 1.9))
                    break
        
        im = ImageGrab.grab()
        results = model(im)
        resultsdf = results.pandas().xyxy[0]

        for i in range(len(resultsdf.name)):
            if resultsdf.name[i] == "bank":
                mid_x = round((resultsdf.xmin[i] + resultsdf.xmax[i]) / 4)
                mid_y = round((resultsdf.ymin[i] + resultsdf.ymax[i]) / 4)
                if mid_x < 833 and mid_x > 317:
                    print(f"({mid_x}, {mid_y}) --> coords within vision --> clicking on bank")
                    randomized_click_bank((mid_x, mid_y))
                    sleep(uniform(5, 10))
                    break
    except:
        print(f"belt not seen --> continuing")
        pass

    randomized_bank_click((752, 357))

def main():
    n_of_trips = 30
    for n in range(n_of_trips):
        banking_first()
        first_trip()
        banking_second()
        second_trip()

if __name__ == "__main__":
    main()

    



    