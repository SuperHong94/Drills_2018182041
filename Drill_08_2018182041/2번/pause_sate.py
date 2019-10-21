import game_framework
import main_state
from pico2d import *


name = "PauseState"
image = None

def enter():
    global  image
    image=load_image('pause.png')

    pass


def exit():
    global image
    del(image)
    pass


def handle_events():
    events=get_events()
    for event in events:
        if event.type==SDL_QUIT:
            game_framework.quit()
        else:
            if(event.type,event.key)==(SDL_KEYDOWN,SDLK_p):
                game_framework.pop_state()

    pass

def update():

    clear_canvas()
    pass

def draw():
    clear_canvas()
    #image.draw(400,300)

    main_state.draw()
    image.draw_to_origin(300, 300, 200, 200)
    update_canvas()
    pass