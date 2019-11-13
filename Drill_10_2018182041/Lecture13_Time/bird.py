import game_framework
from pico2d import *

import game_world

# Boy Run Speed
# fill expressions correctly
PIXEL_PER_METER = (10.0/0.3)    #10 pixel 30cm
RUN_SPEED_KMPH = 20.0           # km /Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
# fill expressions correctly
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 14

# Boy States
class FlyState:
    @staticmethod
    def enter(bird, event):
        bird.dir = 1
        bird.velocity = RUN_SPEED_PPS

    @staticmethod
    def exit(bird, event):
        pass

    @staticmethod
    def do(bird):
        bird.frame = (bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 14
        bird.x += bird.velocity * game_framework.frame_time * bird.dir

        if bird.x >= 1600 - 25:
            bird.dir = -1
        elif bird.x <= 25:
            bird.dir = 1
#bird.pos[int(bird.frame)][1]
    @staticmethod
    def draw(bird):
        if bird.dir == 1:
            bird.image.clip_draw((int(bird.frame) % 5) * 183, 168, 180, 160, bird.x, bird.y)
        else:
            bird.image.clip_composite_draw((int(bird.frame) % 5) * 183,  168,
                                           180, 160, 0.0, 'h', bird.x, bird.y, 180, 160)


class Bird:
    def __init__(self):
        self.x, self.y = 1600 // 2, 400
        # Boy is only once created, so instance image loading is fine
        self.image = load_image('bird_animation.png')
        self.font = load_font('ENCR10B.TTF',16)
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.Y= [2,2,2,2,2,1,1,1,1,1,0,0,0,0,0]
        self.event_que = []
        self.cur_state = FlyState
        self.cur_state.enter(self, None)


    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)
        self.font.draw(self.x - 60, self.y + 50, '(Time: %3.2f)' % get_time(), (255,255,0))