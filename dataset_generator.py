from PIL import ImageGrab
from time import sleep

def screenshotter( training_set_size, coord_left_x, coord_right_x, coord_top_y, coord_bottom_y ):
    """
    Takes screenshots of a pre-specified portion of the screen to later be labeled
    """
    print('starting taking screenshots in 5..')
    sleep(5)
    for index, image in enumerate(range(training_set_size)):
        training_img = ImageGrab.grab(bbox=(coord_left_x, coord_top_y, coord_right_x, coord_bottom_y))
        training_img.save(f'data{index}.png')
        print(f'image no. {index+1} saved..\nchange orientation..')
        sleep(0.5)
    print(f'{index+1} images saved.\nquitting..')

screenshotter(150, 318*2, 1035*2, 52*2, 556*2) # all coord values doubled are doubled due to a macbook's screen res