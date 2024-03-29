import random
import json
import os

from pico2d import *
import game_framework
import game_world

from boy import Boy
from grass import Grass
from ball import Ball, BigBall
from brick import  Brick

name = "MainState"

boy = None
grass = None
balls = []
big_balls = []
brick=None

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True

def BricCollide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    if bottom_b-top_a<-5:return False
    return True

def enter():
    global boy
    boy = Boy()
    game_world.add_object(boy, 1)

    global grass
    grass = Grass()
    game_world.add_object(grass, 0)

    global balls
    balls = [Ball() for i in range(20)]+[BigBall() for i in range(20)]
    game_world.add_objects(balls, 1)
    # fill here for balls
    global brick
    brick= Brick()
    game_world.add_object(brick, 1)

    pass


def exit():
    game_world.clear()


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()
    if collide(boy,grass):
        boy.y+=1
    if collide(boy,brick):
        boy.y+=1
        boy.x+=brick.fall_speed * game_framework.frame_time*brick.dir

    for ball in balls:
        if collide(boy,ball):
            balls.remove(ball)
            game_world.remove_object(ball)
    # fill here for collision check
    for ball in balls:
        if collide(grass,ball):
            ball.stop()
        if BricCollide(brick,ball):
            ball.stop()
            ball.x+=brick.fall_speed * game_framework.frame_time*brick.dir



def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()
