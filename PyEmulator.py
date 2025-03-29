import math
import time
from math import *
import pyautogui
from pyautogui import Point
from pynput import mouse, keyboard
from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import Key
from pynput.mouse import Controller as MouseController

class Main:
    def __init__(self):
        self.mouse = Mouse()
        self.board = KeyboardPressed()

        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()
    def on_key_press(self, key):
        if key.char == 'q' and not self.board.can_pressed:
            print('Включен')
            self.board.can_pressed = True
        elif key.char == 'e' and self.board.can_pressed:
            print('Отключен')
            self.board.can_pressed = False
    def run(self):
        while True:
            if self.mouse.update_mouse():
                self.board.emulate(self.mouse.direction)
            # if keyboard.is_pressed('q') and not self.board.can_pressed:
            #     print('Включен')
            #     self.board.can_pressed = True
            # elif keyboard.is_pressed('e') and self.board.can_pressed:
            #     print('Отключен')
            #     self.board.can_pressed = False
            #
            # if self.mouse.update_mouse():
            #     self.board.emulate(self.mouse.direction)


class KeyboardPressed:
    def __init__(self):
        self.can_pressed = False
        self.last_button = None
        self.keyboard = KeyboardController()
        self.dict = {
            Point(1, 0): 'd',
            Point(0, 1): 'w',
            Point(-1, 0): 'a',
            Point(0, -1): 's',
            Point(-1, 1): 'y',
            Point(1, 1): 'u',
            Point(-1, -1): 'h',
            Point(1, -1): 'j',
            Point(0, 0): None
        }

    def emulate(self, direction: Point):

        if not self.can_pressed:
            if self.last_button is not None:
                self.keyboard.release(self.last_button)
                self.last_button = None
            return

        current_key = self.dict.get((direction.x, direction.y))

        if current_key != self.last_button:
            if self.last_button is not None:
                self.keyboard.release(self.last_button)
            if current_key is not None:
                self.keyboard.press(current_key)
            self.last_button = current_key


class Mouse:
    def __init__(self):
        self.mouse = MouseController()
        self.last_position = self.mouse.position
        self.direction = Point(0, 0)
        self.last_time = time.time()
        self.sign = lambda x: (x > 0) - (x < 0)
        self.angle_threshold = math.radians(20)
    def update_mouse(self) -> bool:
        if time.time() - self.last_time < 0.03:
            return False

        now_position = pyautogui.position()
        delta_x = now_position[0] - self.last_position[0]
        delta_y = self.last_position[1] - now_position[1]

        angle = math.atan2(abs(delta_y), abs(delta_x))
        if angle < self.angle_threshold or angle > (math.pi/2 - self.angle_threshold):
            if abs(delta_x) > abs(delta_y):
                self.direction = Point(self.sign(delta_x), 0)
            else:
                self.direction = Point(0, self.sign(delta_y))
        else:
            self.direction = Point(self.sign(delta_x), self.sign(delta_y))

        self.last_position = now_position
        self.last_time = time.time()
        # self.last_position = now_position
        # self.last_time = time.time()
        # self.direction = Point(self.sign(delta_x), self.sign(delta_y))
        # self.last_position = now_position
        # self.last_time = time.time()
        return True


if __name__ == '__main__':
    Main().run()