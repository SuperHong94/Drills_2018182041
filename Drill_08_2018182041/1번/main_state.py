import random
import json
import os

from pico2d import *

import game_framework
import title_state
import pause_sate


name = "MainState"

boy = None
grass = None
font = None



class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)



class Boy:
    def __init__(self):
        self.x, self.y = 0, 90
        self.frame = 0
        self.image = load_image('animation_sheet.png')
        self.dir = 1
        self.direction=False

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.x += self.dir
        if self.x >= 800:  #왼쪽
            self.direction=True
            self.dir = -1
        elif self.x <= 0:
            self.direction=False
            self.dir = 1

    def draw(self):
        if self.direction:
            self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)  #왼쪽
        else:
            self.image.clip_draw(self.frame * 100, 100, 100, 100, self.x, self.y)


def enter():
    global boy,grass
    boy=Boy()
    grass=Grass()
    pass


def exit():
    global boy,grass
    del(boy)
    del(grass)
    pass


def pause():
    pass


def resume():
    pass


def handle_events():
    events=get_events()
    for event in events:
        if event.type==SDL_QUIT:
            game_framework.quit()
        elif event.type==SDL_KEYDOWN and event.key==SDLK_ESCAPE:
            game_framework.change_state(title_state)
        elif event.type==SDL_KEYDOWN and event.key==SDLK_p:
            game_framework.push_state(pause_sate)
    pass


def update():
    boy.update()
    pass


def draw():
    clear_canvas()
    grass.draw()
    boy.draw()
    update_canvas()
    pass





