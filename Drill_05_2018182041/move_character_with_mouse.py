from pico2d import *


KPU_WIDTH, KPU_HEIGHT = 1280, 600
open_canvas(KPU_WIDTH, KPU_HEIGHT)
kpu_ground = load_image('KPU_GROUND.png')
character = load_image('animation_sheet.png')
myMouse=load_image('hand_arrow.png')


def handle_events():
    global running
    global myClick
    global x, y
    global endX,endY
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_MOUSEMOTION:
            x, y = event.x+35, KPU_HEIGHT - 1 - event.y-45
        elif event.type==SDL_MOUSEBUTTONDOWN:
            endX, endY = event.x + 20, KPU_HEIGHT - 1 - event.y - 20
            myClick=True
        #elif event.type==SDL_MOUSEBUTTONUP:

        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

    pass



running = True
x, y = KPU_WIDTH // 2, KPU_HEIGHT // 2
endX, endY = KPU_WIDTH // 2, KPU_HEIGHT // 2
myClick=False
cX=100
cY=100
fx=100
fy=100
global dir
dir=fx-cX
hide_cursor()

frame=0
while running:
    clear_canvas()
    kpu_ground.draw(KPU_WIDTH // 2, KPU_HEIGHT // 2)
    myMouse.clip_draw(0, 0, 100, 100, x, y)
    if dir >= 0:
        character.clip_draw(frame * 100, 100, 100, 100, cX, cY)
    else:
        character.clip_draw(frame * 100, 0, 100, 100, cX, cY)
    frame = (frame + 1) % 8
    update_canvas()
    while(myClick):
        clear_canvas()
        kpu_ground.draw(KPU_WIDTH // 2, KPU_HEIGHT // 2)
        myMouse.clip_draw(0, 0, 100, 100, x, y)
        frame = (frame + 1) % 8
        for i in range(0,100+1,2):
            dir = fx - cX
            clear_canvas()
            kpu_ground.draw(KPU_WIDTH // 2, KPU_HEIGHT // 2)
            myMouse.clip_draw(0, 0, 100, 100, x, y)
            t = i / 100
            fx = (1 - t) * cX + t * endX
            fy = (1 - t) * cY + t * endY
            if dir>=0:
                character.clip_draw(frame * 100, 100, 100, 100, fx-20, fy+10)
            else:
                character.clip_draw(frame * 100, 0, 100, 100, fx-20, fy+10)
            frame = (frame + 1) % 8
            delay(0.02)
            update_canvas()


        cX=endX-20
        cY=endY+10
        myClick=False

    handle_events()

close_canvas()
