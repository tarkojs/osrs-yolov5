import pyautogui as pya
from random import randint, uniform
from time import sleep, time
from PIL import ImageGrab

# the 'Player' class contains all player interactions

class Player():

    def __init__(self, model):
        self.model = model
        self.model.conf = 0.7
        self.iou = 0.45
        self.agnostic = False
        self.multi_label = False
        self.classes = None
        self.max_det = 10
        self.amp = False
        self.tot = 0
        

    def get_live_image(self):
        """
        Returns the dataframe of all current detections
        """
        live_img = ImageGrab.grab()
        results = self.model(live_img)
        results_df = results.pandas().xyxy[0]
        return results_df


    def get_detected_names(self):
        """
        Returns the names of all current detections
        """
        return self.get_live_image().name


    def check_if_in_action(self):
        """
        Returns the number of objects currently detected
        """
        return len(self.get_detected_names())


    def mining_check_if_inv_full(self):
        """
        Currently checks by iterating through the results dataframe
        """
        try:
            image = self.get_live_image()
            for index, detection in enumerate(image.name):
                if image.name[index] == 'time_to_drop':
                    if image.confidence[index] >= 0.6:
                        print(f'dropping.. -> confidence: {round(image.confidence[index]), 2}')
                        self.drop_ores()
                        self.sleep_custom('between-action-short')
                        break
        except Exception: print('inventory not considered full.')


    def willows_check_if_inv_full(self):
        """
        Currently checks by iterating through the results dataframe
        """
        try:
            image = self.get_live_image()
            for index, detection in enumerate(image.name):
                if image.name[index] == 'invfull':
                    if image.confidence[index] >= 0.7:
                        print(f'inventory full.. -> confidence: {round(image.confidence[index]), 2}')
                        self.drop_all()
                        self.sleep_custom('big-interval-short')
                        break
        except Exception: print('inventory not considered full.')

    
    def barb_check_for_next_action(self):
        """
        Currently checks by iterating through the results dataframe
        """
        try:
            image = self.get_live_image()
            for index, detection in enumerate(image.name):
                if image.name[index] == 'invfull':
                    if image.confidence[index] >= 0.3:
                        print(f'dropping.. -> confidence: {round(image.confidence[index]), 2}')
                        self.drop_all()
                        self.sleep_custom('big-interval-short')
                        break
                if image.name[index] == 'is_fishing':
                    while True:
                        image = self.get_live_image()
                        for index, detection in enumerate(image.name):
                            if image.name[index] == 'is_fishing':  
                                print(f'still fishing.. -> confidence: {round(image.confidence[index]), 2}')
                                self.sleep_custom('barb-fishing')
                                break
        except Exception: print('error in checking for next action..')
                    

    def barb_check_if_click_available(self):
        """
        Checks again if the character is not in action
        Returns True if click is available
        """
        fish_list = []
        try:
            image = self.get_live_image()
            for index, detection in enumerate(image.name):
                if image.name[index] == 'is_fishing':
                    fish_list.append(image.name[index])
            if 'is_fishing' not in fish_list: return True
            elif 'is_fishing' in fish_list: return False
        except Exception: print('error in checking for click availability')


    def get_click_location(self, randomize_x, randomize_y):
        """
        Gets the location of the detection
        Randomizes this location and returns the randomized coordinates
        """
        try:
            image = self.get_live_image()
            mid_x = round((image.xmin[0] + image.xmax[0]) / 4) # divided by 2 to get the centers of the boxes
            mid_y = round((image.ymin[0] + image.ymax[0]) / 4) # divided by 2 again due to the screenshots being 2880x1800, the actual res is 1440x900
            randomize = randint(-randomize_x, randomize_x)
            randomize_ = randint(-randomize_y, randomize_y)
            coords_randomized = (mid_x + randomize, mid_y + randomize_)
            print(f'\n...\nfound coords -> {coords_randomized}\n1st randomization -> {randomize}\n2nd randomization -> {randomize_}\n...\n')
            return coords_randomized
        except Exception: print('no available coords found..')


    def click_on_detected_loc(self, randomize_x, randomize_y):
        """
        Clicks on the randomized coordinates
        """
        try:
            pya.moveTo(self.get_click_location(randomize_x, randomize_y))
            pya.click()
        except Exception:
            print('unable to click.. continuing..')
            pass


    def sleep_custom(self, sleep_name_string):
        """
        Argument specified as a string
        "drop" -> sleep in-between dropping ores
        "between-mine" -> sleep in-between mining
        "reiteration" -> sleep before starting another iteration of the main loop
        """
        try:
            if sleep_name_string == 'drop':
                rand = round(uniform(0.03, 0.145), 2)
                print(f'drop sleep called -> sleeping for {rand} seconds..')
                return sleep(rand)
            if sleep_name_string == 'between-action-short':
                rand = round(uniform(0.89, 1.21), 2)
                print(f'between-action-short sleep called -> sleeping for {rand} seconds..')
                return sleep(rand)
            if sleep_name_string == 'long':
                rand = round(uniform(7, 16), 2)
                print(f'long sleep called -> sleeping for {rand} seconds..')
                return sleep(rand)
            if sleep_name_string == 'willows':
                rand = round(uniform(7, 9), 2)
                print(f'\n***\nwillows sleep called -> sleeping for {rand} seconds..\n***\n')
                return sleep(rand)
            if sleep_name_string == 'barb-fishing':
                rand = round(uniform(1, 15), 2)
                print(f'\n***\nbarb fishing sleep called -> sleeping for {rand} seconds..\n***\n')
                return sleep(rand)
            if sleep_name_string == 'big-interval-short':
                rand = round(uniform(0.2, 1.1), 2)
                print(f'\n***\nbig-interval-short sleep called -> sleeping for {rand} seconds..\n***\n')
                return sleep(rand)
            if sleep_name_string == 'reiteration':
                rand = round(uniform(0, 1.2), 2)
                print(f'\n***\nreiteration sleep called -> sleeping for {rand} seconds..\n***\n')
                return sleep(rand)
            if sleep_name_string == 'inactivity-sleep':
                rand = round(uniform(0.15, 6.24), 2)
                print(f'\n***\ninactivity sleep called -> sleeping for {rand} seconds..\n***\n')
                return sleep(rand)
        except NameError: print(f'{sleep_name_string} is not a valid input for sleep_custom.')
        except Exception: pass


    def randomize_drop_coord(self):
        """
        Randomizes inventory-item drop coordinates
        Works as an anti-ban
        """
        rand = randint(-13, 13)
        rand_ = randint(-13, 13)
        rand_rand = (rand, rand_)
        return rand_rand


    def drop_ores(self):
        """
        Drops the first three ores in your inventory
        Idea -> implement in a loop
        """
        temp_coords = self.randomize_drop_coord()
        moved_to = pya.moveTo( 897 + temp_coords[0], 279 + temp_coords[1] )
        print(f'dropping ore at -> {moved_to}, added randomness -> **{temp_coords}**')
        self.drop()

        temp_coords = self.randomize_drop_coord()
        moved_to = pya.moveTo( 940 + temp_coords[0], 279 + temp_coords[1] )
        print(f'dropping ore at -> {moved_to}, added randomness -> **{temp_coords}**')
        self. drop()

        temp_coords = self.randomize_drop_coord()
        moved_to = pya.moveTo( 983 + temp_coords[0], 279 + temp_coords[1] )
        print(f'dropping ore at -> {moved_to}, added randomness -> **{temp_coords}**')
        self.drop()


    def drop_all(self):
        """
        Drops all the items in your inventory
        """

        print('preparing to drop all items..\nsleeping..')
        self.sleep_custom('long')
        print('dropping..')

        pya.moveTo((1240 + self.randomize_drop_coord()[0], 280 + randint(-10,10)))
        pya.click()

        pya.moveTo((898 + self.randomize_drop_coord()[0], 280 + self.randomize_drop_coord()[1]))
        self.drop()
        pya.moveTo((940 + self.randomize_drop_coord()[0], 280 + self.randomize_drop_coord()[1]))
        self.drop()
        pya.moveTo((982 + self.randomize_drop_coord()[0], 280 + self.randomize_drop_coord()[1]))
        self.drop()
        pya.moveTo((1023 + self.randomize_drop_coord()[0], 280 + self.randomize_drop_coord()[1]))
        self.drop()

        pya.moveTo((898 + self.randomize_drop_coord()[0], 317 + self.randomize_drop_coord()[1]))
        self.drop()
        pya.moveTo((940 + self.randomize_drop_coord()[0], 317 + self.randomize_drop_coord()[1]))
        self.drop()
        pya.moveTo((982 + self.randomize_drop_coord()[0], 317 + self.randomize_drop_coord()[1]))
        self.drop()
        pya.moveTo((1023 + self.randomize_drop_coord()[0], 317 + self.randomize_drop_coord()[1]))
        self.drop()

        pya.moveTo((898 + self.randomize_drop_coord()[0], 354 + self.randomize_drop_coord()[1]))
        self.drop()
        pya.moveTo((940 + self.randomize_drop_coord()[0], 354 + self.randomize_drop_coord()[1]))
        self.drop()
        pya.moveTo((982 + self.randomize_drop_coord()[0], 354 + self.randomize_drop_coord()[1]))
        self.drop()
        pya.moveTo((1023 + self.randomize_drop_coord()[0], 354 + self.randomize_drop_coord()[1]))
        self.drop()

        pya.moveTo((898 + self.randomize_drop_coord()[0], 390 + self.randomize_drop_coord()[1]))
        self.drop()
        pya.moveTo((940 + self.randomize_drop_coord()[0], 390 + self.randomize_drop_coord()[1]))
        self.drop()
        pya.moveTo((982 + self.randomize_drop_coord()[0], 390 + self.randomize_drop_coord()[1]))
        self.drop()
        pya.moveTo((1023 + self.randomize_drop_coord()[0], 390 + self.randomize_drop_coord()[1]))
        self.drop()

        pya.moveTo((898 + self.randomize_drop_coord()[0], 425 + self.randomize_drop_coord()[1]))
        self.drop()
        pya.moveTo((940 + self.randomize_drop_coord()[0], 425 + self.randomize_drop_coord()[1]))
        self.drop()
        pya.moveTo((982 + self.randomize_drop_coord()[0], 425 + self.randomize_drop_coord()[1]))
        self.drop()
        pya.moveTo((1023 + self.randomize_drop_coord()[0], 425 + self.randomize_drop_coord()[1]))
        self.drop()

        pya.moveTo((898 + self.randomize_drop_coord()[0], 460 + self.randomize_drop_coord()[1]))
        self.drop()
        pya.moveTo((940 + self.randomize_drop_coord()[0], 460 + self.randomize_drop_coord()[1]))
        self.drop()
        pya.moveTo((982 + self.randomize_drop_coord()[0], 460 + self.randomize_drop_coord()[1]))
        self.drop()
        pya.moveTo((1023 + self.randomize_drop_coord()[0], 460 + self.randomize_drop_coord()[1]))
        self.drop()

        pya.moveTo((898 + self.randomize_drop_coord()[0], 497 + self.randomize_drop_coord()[1]))
        self.drop()
        pya.moveTo((940 + self.randomize_drop_coord()[0], 497 + self.randomize_drop_coord()[1]))
        self.drop()
        pya.moveTo((982 + self.randomize_drop_coord()[0], 497 + self.randomize_drop_coord()[1]))
        self.drop()
        pya.moveTo((1023 + self.randomize_drop_coord()[0], 497 + self.randomize_drop_coord()[1]))
        self.drop()


    def drop(self):
        """
        The actual implementation of dropping
        Idea -> don't release shift unless index of ore in the list is -1 (requires a for loop impl. in drop_ores())
        """
        pya.keyDown('shift')
        self.sleep_custom('drop')
        pya.click()
        self.sleep_custom('drop')
        pya.keyUp('shift')


    def time_setup(self, action: str):
        """
        Returns the current time
        """
        if action == 'current':
            return time()
        