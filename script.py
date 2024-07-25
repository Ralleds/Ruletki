import time
import numpy as np
import pyscreenshot as ImageGrab
import cv2 as cv
import pyautogui
import keyboard
from ctypes  import *


# записываем размеры монитора
x, y = windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)

# отключение автокликов, если увести мышку на координаты 1,1
pyautogui.FAILSAFE = True

# исходники предметов из рулетки
# [[ПУТЬ, ЦВЕТ, ТРЕШХОЛД]]
templates = [[r'loot/fam_talon.png', (0, 0, 240),0.65,32000], [r'loot/money.png', (10, 138, 10),0.5,0],
             [r'loot/narko.png', (255, 255, 255),0.7,1000], [r'loot/podarok.png', (140, 95, 220),0.7,16000],
             [r'loot/exp.png', (200, 100, 100),0.85,0], [r'loot/material.png', (159, 140, 170),0.7,0],
             [r'loot/tabletka.png', (128, 128, 128),0.9,0], [r'loot/az.png', (20, 200, 200),0.8,25000]]

# словарь предметов и уникальных ему цветов
items = {'Семейный талон':[],
         'Наркотики':[],
         'Талон опыта':[],
         'Таблетка адреналина':[],
         'Деньги':[],
         'Подарок':[],
         'Материал':[],
         'AZ-Coin':[],}

present = [[[38, 26], [195, 191, 24]],[[25, 29], [231, 0, 0]]]

# реализация класса под объекты, объектом будет каждый айтем в рулетке, на все 16
# положение, предмет, флаг на исчесляемость, количество, редкость?


def spin():
    time.sleep(1)

    pyautogui.mouseDown(895, 606)
    time.sleep(0.2)
    pyautogui.mouseUp()

    return


def reroll():
    time.sleep(1)

    pyautogui.mouseDown(1055, 590)
    time.sleep(0.2)
    pyautogui.mouseUp()

    time.sleep(1)

    pyautogui.mouseDown(895, 592)
    time.sleep(0.2)
    pyautogui.mouseUp()

    return


# функция для определения типа рулетки, принимает скриншот экрана, возвращает выбранный тип строкой
def rulet_check(screenshot):
    dicts = {712:'bronze', 833:'silver', 949:'gold', 1090:'platinum'}

    for key, value in dicts.items():
        pixel = screenshot[302, key]
        if pixel[0] != 153 or pixel[1] != 69 or pixel[2] != 69:
            return value


def find_items():
    # делаем свой скрин, в нужной области (ббокс)

    screenshot = ImageGrab.grab(bbox=(int(x / 3.92), int(y / 3.22), int(x / 1.43), int(y / 1.97)))
    screenshot = np.array(screenshot)
    screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)

    loot = []
    # прогоняем поиск каждого объекта на скрине, чтобы найти все объекты
    for temp in templates:
        ## screenshot, count = finding_objects(screenshot, temp)
        count = finding_objects(screenshot, temp)
        loot.append([temp[0], count, temp[3]])
    # read_text(screenshot)
    return loot
    ##cv.imshow('Тест', screenshot)
    ##cv.waitKey()


def finding_objects(img, temp):
    # Считываем файл с основным изображением
    img_rgb = img
    # Считываем файл с объектом поиска
    template = cv.imread(temp[0], 0)

    # Размер объекта поиска
    temp_w, temp_h = template.shape[::-1]
    # Задаём трешхолд
    threshold = temp[2]

    # Основное изображение конвертим в серое
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)

    # Поиск образца в на изображении
    result = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    # Выбираем локации, подходящие под трешхолд
    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))

    # Создаём список объектов для группировки
    rectangles = []
    for loc in locations:
        rect = [int(loc[0]), int(loc[1]), temp_w, temp_h]
        rectangles.append(rect)

    # Группировка объектов
    rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)

    '''
    # Считаем и отрисовываем найденные объекты
    ##if len(rectangles):
        # Цвет линий обводки
    ##    line_color = temp[1]
        # Размер обводки
    ##    line_type = cv.LINE_4

    ##    for (x, y, w, h) in rectangles:
            # Создание обводки
    ##        top_left = (x, y)
    ##        bottom_right = (x + w, y + h)
    ##        cv.rectangle(img_rgb, top_left, bottom_right, line_color, line_type)

    #read_text(img_rgb)
    #return img_rgb, len(rectangles)
    '''
    return len(rectangles)


'''
def read_text(screen):
    sharp_filter = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])

    self_screenshot = screen
    #self_screenshot = ImageGrab.grab(bbox=(int((x / 3.92) + x_start + 18), int((y / 3.22) + y_start + 47),
    #                                       int((x / 3.92) + x_start + 66), int((y / 3.22) + y_start + 64)))
    self_screenshot = cv.pyrUp(self_screenshot)
    self_screenshot = cv.pyrUp(self_screenshot)
    self_screenshot = cv.filter2D(self_screenshot, ddepth=-1, kernel=sharp_filter)

    img_count = np.uint8(np.zeros((self_screenshot.shape[0],self_screenshot.shape[1])))

    hsv = cv.cvtColor(self_screenshot, cv.COLOR_RGB2HSV)

    lower = np.array([0, 0, 234])
    upper = np.array([161, 20, 255])

    mask = cv.inRange(hsv, lower, upper)

    #self_screenshot = cv.pyrUp(self_screenshot)
    #self_screenshot = cv.pyrUp(self_screenshot)
    #self_screenshot = cv.filter2D(self_screenshot, ddepth=-1, kernel=sharp_filter)
    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    cv.drawContours(img_count, contours, -1, (255, 255, 255), 2)

    cv.imshow('test', img_count)
    cv.waitKey()

    #self_screenshot = cv.pyrUp(self_screenshot)

    cv.imwrite('text.png', img_count)
    reader = easyocr.Reader(["en"])
    result = reader.readtext('text.png', allowlist='$0123456789', detail=1, min_size=1, text_threshold=0.1)
    print(result)'''


# создание скриншотов экрана, перевод в нампи массив и возврат его как объект компьютерного зрения
def window_capture():
    screenshot = ImageGrab.grab()
    return np.array(screenshot)


def check_state(loot):

    time.sleep(1)

    pyautogui.mouseDown(1100, 310)
    time.sleep(0.2)
    pyautogui.mouseUp()

    time.sleep(0.2)

    pyautogui.mouseDown(714, 312)
    time.sleep(0.2)
    pyautogui.mouseUp()

    time.sleep(0.2)
    new_loot = find_items()
    time.sleep(0.2)

    print('Лут не изменился' if loot == new_loot else 'Лут изменился!')
    return loot == new_loot


def break_script():
    try:
        if keyboard.is_pressed('q'):  # it will stop working by clicking q you can change to to any key
            exit()
        else:
            pass
    finally:
        pass


def main():
                    # берём скриншот всего экрана
                    ##full_screen = window_capture()
                    # вызываем функцию рулет_чек чтобы узнать тип выбранной рулетки
                    ##selected_rullet = rulet_check(full_screen)

                    #print(selected_rullet)

    while True:

        break_script()

        podarki = False

        time.sleep(0.2)

        loot = find_items()
        # value = 0

        for item in loot:
            if item[0] == 'loot/podarok.png' and item[1] > 4:
                podarki = True

            # value += item[1] * item[2]


        if not podarki:
            break_script()

            print('Не найдено достаточно подарков, производится спин и реролл')
            time.sleep(1)
            spin()
            time.sleep(1)
            reroll()
        else:
            print('Найдено 5+ подарков, начинаю фармить')

            while check_state(loot):

                for _ in range(10):
                    spin()

                    break_script()


if __name__ == '__main__':
    main()