import pyautogui as pya
from time import sleep
from random import uniform, randint


def customsleep(inp = int):
        try:
            if inp == 0:
                rand = round(uniform(0.03, 0.25), 3)
                print(f"mini sleep called - sleeping for {rand} seconds")
                return sleep(rand)
            if inp == 1:
                rand = round(uniform(0.3, 0.9), 3)
                print(f"short sleep called - sleeping for {rand} seconds")
                return sleep(rand)
            if inp == 2:
                rand = round(uniform(0.2, 1.1), 3)
                print(f"mid sleep called - sleeping for {rand} seconds")
                return sleep(rand)
            if inp == 3:
                rand = round(uniform(1.2, 3.5), 3)
                print(f"long sleep called - sleeping for {rand} seconds")
                return sleep(rand)
            if inp == 4:
                rand = round(uniform(7, 16), 3)
                print(f"properly long sleep called - sleeping for {rand} seconds")
                return sleep(rand)
        except NameError:
            return ("Use an integer as input for customsleep")


def drop_logs():

    # idea --> automate coords
    
    print("starting to drop logs - change x and y values if incorrect")
    customsleep(4)

    pya.moveTo((1240 + randint(-10, 10), 280 + randint(-10,10)))
    pya.click()

    pya.moveTo((898 + randint(-10, 10), 280 + randint(-10, 10)))
    drop()
    pya.moveTo((940 + randint(-10, 10), 280 + randint(-10, 10)))
    drop()
    pya.moveTo((982 + randint(-10, 10), 280 + randint(-10, 10)))
    drop()
    pya.moveTo((1023 + randint(-10, 10), 280 + randint(-10, 10)))
    drop()

    pya.moveTo((898 + randint(-10, 10), 317 + randint(-10, 10)))
    drop()
    pya.moveTo((940 + randint(-10, 10), 317 + randint(-10, 10)))
    drop()
    pya.moveTo((982 + randint(-10, 10), 317 + randint(-10, 10)))
    drop()
    pya.moveTo((1023 + randint(-10, 10), 317 + randint(-10, 10)))
    drop()

    pya.moveTo((898 + randint(-10, 10), 354 + randint(-10, 10)))
    drop()
    pya.moveTo((940 + randint(-10, 10), 354 + randint(-10, 10)))
    drop()
    pya.moveTo((982 + randint(-10, 10), 354 + randint(-10, 10)))
    drop()
    pya.moveTo((1023 + randint(-10, 10), 354 + randint(-10, 10)))
    drop()

    pya.moveTo((898 + randint(-10, 10), 390 + randint(-10, 10)))
    drop()
    pya.moveTo((940 + randint(-10, 10), 390 + randint(-10, 10)))
    drop()
    pya.moveTo((982 + randint(-10, 10), 390 + randint(-10, 10)))
    drop()
    pya.moveTo((1023 + randint(-10, 10), 390 + randint(-10, 10)))
    drop()

    pya.moveTo((898 + randint(-10, 10), 425 + randint(-10, 10)))
    drop()
    pya.moveTo((940 + randint(-10, 10), 425 + randint(-10, 10)))
    drop()
    pya.moveTo((982 + randint(-10, 10), 425 + randint(-10, 10)))
    drop()
    pya.moveTo((1023 + randint(-10, 10), 425 + randint(-10, 10)))
    drop()

    pya.moveTo((898 + randint(-10, 10), 460 + randint(-10, 10)))
    drop()
    pya.moveTo((940 + randint(-10, 10), 460 + randint(-10, 10)))
    drop()
    pya.moveTo((982 + randint(-10, 10), 460 + randint(-10, 10)))
    drop()
    pya.moveTo((1023 + randint(-10, 10), 460 + randint(-10, 10)))
    drop()

    pya.moveTo((898 + randint(-10, 10), 497 + randint(-10, 10)))
    drop()
    pya.moveTo((940 + randint(-10, 10), 497 + randint(-10, 10)))
    drop()
    pya.moveTo((982 + randint(-10, 10), 497 + randint(-10, 10)))
    drop()
    pya.moveTo((1023 + randint(-10, 10), 497 + randint(-10, 10)))
    drop()

def drop():
    pya.keyDown("shift")
    customsleep(0)
    pya.click()
    customsleep(0)
    pya.keyUp("shift")


