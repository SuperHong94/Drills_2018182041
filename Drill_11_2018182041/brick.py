import game_framework
import random
from pico2d import *

class Brick:
    image = None

    def __init__(self):
        if Brick.image == None:
            Brick.image = load_image('brick180x40.png')
        self.x, self.y, self.fall_speed = random.randint(0, 1600-1), 200,200
        self.dir=1

    def get_bb(self):
        # fill here
        return self.x - 90, self.y - 20, self.x + 90, self.y + 20

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())
        # fill here for draw

    def update(self):
        if self.x-90<0:
            self.dir=1
        elif self.x+90>get_canvas_width():
            self.dir=-1
        self.x += self.fall_speed * game_framework.frame_time*self.dir
        pass

    #fill here for def stop