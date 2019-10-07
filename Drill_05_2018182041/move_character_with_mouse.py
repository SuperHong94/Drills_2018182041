from pico2d import *

KPU_WIDTH, KPU_HEIGHT = 1280, 600


def handle_events():
    global running
    global x, y
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_MOUSEMOTION:
            x, y = event.x+20, KPU_HEIGHT - 1 - event.y-10
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

    pass


open_canvas(KPU_WIDTH, KPU_HEIGHT)
kpu_ground = load_image('KPU_GROUND.png')
character = load_image('animation_sheet.png')
myMouse=load_image('hand_arrow.png')
running = True
x, y = KPU_WIDTH // 2, KPU_HEIGHT // 2
frame = 0
#hide_cursor()

while running:
    clear_canvas()
    kpu_ground.draw(KPU_WIDTH // 2, KPU_HEIGHT // 2)
    myMouse.clip_draw(0, 0, 100, 100, x, y)
    update_canvas()
    #delay(0.02)
    handle_events()

close_canvas()
