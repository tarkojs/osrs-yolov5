from character import Player
from random import randint
import torch
import sys

"""
Run any script using this Python file
Please specify the script you would like to use on the line below
"""

script = 'willows' # specify the script you would like to use -> ('willows'/'barbarian_fishing'/'blast_furnace')

def setup_model(script: str):
    try:
        if script == 'willows': model_setup = '/Users/tarkojuss/Desktop/vskoodkood/OSTreeDetection/model_weights/best_willows.pt'
        elif script == 'barbarian_fishing': model_setup = '/Users/tarkojuss/Desktop/vskoodkood/OSTreeDetection/model_weights/best_barb_fish.pt'
        elif script == 'blast_furnace': model_setup = '/Users/tarkojuss/Desktop/vskoodkood/OSTreeDetection/model_weights/best_blast_furnace.pt'
        else: sys.exit('quitting due to an error in model setup..')
        return model_setup
    except:
        print(f'"{script}" is not a valid name for a script.')
        sys.exit('quitting due to an error in model setup..')

# cmnd for detection testing:: python detect.py --/users/tarkojuss/miner-osrs/weights_best.pt --img 300 --conf 0.2 --source 0

def script_willows():
    char = Player( torch.hub.load('ultralytics/yolov5', 'custom', setup_model(script)))
    while True:
        randroll = randint(30, 60)
        c = 0
        start_timecount = char.time_setup('current')
        char.willows_check_if_inv_full()
        char.click_on_detected_loc()
        time_total = 0
        char.sleep_custom('willows')
        while True:
            detection_begin = char.check_if_in_action()
            print(f'initial number of detections -> {detection_begin}')
            while True:
                time_start = char.time_setup('current')
                detection_check = char.check_if_in_action()
                print(f'current number of detections -> {detection_check}, time left to trigger inactivity -> {round(abs(randroll - time_total))}')
                c += 1
                if time_total > randroll:
                    print(f'feeling stagnant -> continuing..')
                    break
                if detection_begin != detection_check:
                    print(f'character considered inactive due to a difference in detection: {detection_begin} =/= {detection_check}')
                    char.sleep_custom('inactivity-sleep')
                    break
                if c > randroll:
                    print(f'character considered inactive due to high count -> {c}')
                    char.sleep_custom('inactivity-sleep')
                    break
                char.willows_check_if_inv_full()
                time_end = char.time_setup('current')
                time_total = (time_end - time_start)
                time_end = 0
                time_start = 0
            break
        end_timecount = char.time_setup('current')
        char.tot += (end_timecount - start_timecount)
        end_timecount = 0
        start_timecount = 0


def script_barb_fishing():
    char = Player( torch.hub.load('ultralytics/yolov5', 'custom', setup_model(script)))
    pass


def script_blast_furnace():
    char = Player( torch.hub.load('ultralytics/yolov5', 'custom', setup_model(script)))
    pass


def script_mining():
    """
    Not finished to an acceptable degree
    """
    char = Player( torch.hub.load('ultralytics/yolov5', 'custom', setup_model(script)))
    while True:
        char.drop_ores()
        char.sleep_custom('reiterating main loop..')
        print('reiterating the process.. -> reiteration sleep')


def main(): 
    print(f'setting up script -> {script}')
    if script == 'willows': script_willows()
    elif script == 'barbarian_fishing': script_barb_fishing()
    elif script == 'blast_furnace': script_blast_furnace()
    else: sys.exit('quitting due to an error in the main block..')


if __name__ == '__main__':
    main()