import random
import math
import game_framework
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
from pico2d import *
import main_state

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10

animation_names = ['Attack', 'Dead', 'Idle', 'Walk']


class Zombie:
    images = None

    def load_images(self):
        if Zombie.images == None:
            Zombie.images = {}
            for name in animation_names:
                Zombie.images[name] = [load_image("./zombiefiles/female/" + name + " (%d)" % i + ".png") for i in
                                       range(1, 11)]

    def __init__(self):
        self.x, self.y = 1280 / 4 * 3, 1024 / 4 * 3

        self.target_x, self.target_y = None, None

        self.load_images()
        self.dir = random.random() * 2 * math.pi  # random moving direction
        self.speed = 0
        self.timer = 1.0  # change direction every 1 sec when wandering
        self.frame = 0
        self.build_behavior_tree()
        self.font = load_font('ENCR10B.TTF', 16)
        self.draw_bool = True

        self.HP = 500

    def calculate_current_position(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        self.x = clamp(50, self.x, 1280 - 50)
        self.y = clamp(50, self.y, 1024 - 50)

    def wander(self):
        # fill here

        self.speed = RUN_SPEED_PPS
        self.calculate_current_position()
        self.timer -= game_framework.frame_time
        if self.timer < 0:
            self.timer += 1.0
            self.dir = random.random() * 2 * math.pi
        return BehaviorTree.SUCCESS
        pass

    def find_player(self):
        # fill here
        boy = main_state.get_boy()
        distance = (boy.x - self.x) ** 2 + (boy.y - self.y) ** 2
        if distance < (PIXEL_PER_METER * 10) ** 2:
            self.dir = math.atan2(boy.y - self.y, boy.x - self.x)

            return BehaviorTree.SUCCESS
        else:
            self.speed = 0
            return BehaviorTree.FAIL
        pass
    def find_ball(self):
        # fill here
        balls = [*main_state.get_ball()]
        min=10000
        for ball in balls:
            distance = (ball.x - self.x) ** 2 + (ball.y - self.y) ** 2
            if distance < (PIXEL_PER_METER * 10) ** 2:
                self.target_x, self.target_y =self.x,self.y
                self.dir = math.atan2(ball.y - self.y, ball.x - self.x)
                return BehaviorTree.SUCCESS
            else:
                self.speed = 0
                return BehaviorTree.FAIL
        pass

    def move_to_player(self):
        # fill here
        boy = main_state.get_boy()
        if boy.HP<self.HP:
            self.speed = RUN_SPEED_PPS
        else:
            self.speed = -RUN_SPEED_PPS
        self.calculate_current_position()
        return BehaviorTree.SUCCESS
        pass

    def move_to_ball(self):
        # fill here
        print("dkdkdkd")
        self.speed = RUN_SPEED_PPS*2
        self.calculate_current_position()
        distance = (self.target_x - self.x) ** 2 + (self.target_y - self.y) ** 2
        if distance < PIXEL_PER_METER ** 2:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING
        return BehaviorTree.RUNNING

        pass

    def get_next_position(self):
        # fill here
        self.target_x, self.target_y = self.patrol_positions[self.patrol_order % len(self.patrol_positions)]
        self.patrol_order += 1
        self.dir = math.atan2(self.target_y - self.y, self.target_x - self.x)
        return BehaviorTree.SUCCESS
        pass

    def move_to_target(self):
        # fill here
        self.speed = RUN_SPEED_PPS
        self.calculate_current_position()
        distance = (self.target_x - self.x) ** 2 + (self.target_y - self.y) ** 2
        if distance < PIXEL_PER_METER ** 2:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING
        pass

    # def runAway_to_player(self):
    #     self.speed=RUN_SPEED_PPS
    #     self.calculate_current_position()
    #     distance=(self.target_x-self.x)**2+(self.target_y-self.y)**2
    #     if distance>PIXEL_PER_METER**2:
    #         return BehaviorTree.SUCCESS
    #     else:
    #         return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        # fill here

        # find_player_node=LeafNode("Find Player",self.find_player)
        # move_to_player_node=LeafNode("Move to Player",self.move_to_player)
        # chase_node=SequenceNode("Chase")
        # chase_node.add_children(find_player_node,move_to_player_node)
        # wander_chase_node=SelectorNode("WanderCahse")
        # wander_chase_node.add_children(chase_node,wander_node)
        # self.bt=BehaviorTree(wander_chase_node)
        wander_node = LeafNode("Wander", self.wander)
        find_player_node = LeafNode("Find Player",self.find_player)
        find_ball_node = LeafNode("Find Ball", self.find_ball)
        move_to_player_node = LeafNode("Move to Player", self.move_to_player)
        move_to_ball_node = LeafNode("Move to Ball", self.move_to_ball)
        zombieAI_node = SelectorNode("ZombieAI")
        chase_or_runAway_node = SequenceNode("COR")
        chase_ball_node = SequenceNode("Chase Ball")
        zombieAI_node.add_children(chase_or_runAway_node, chase_ball_node, wander_node)
        chase_or_runAway_node.add_children(find_player_node, move_to_player_node)

        #공찾기 좀비
        chase_ball_node.add_children(find_ball_node, move_to_ball_node)


        self.bt = BehaviorTree(zombieAI_node)

        pass

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def update(self):
        # fill here
        self.bt.run()
        pass

    def draw(self):
        if self.draw_bool:
            if math.cos(self.dir) < 0:
                if self.speed == 0:
                    Zombie.images['Idle'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 100, 100)
                else:
                    Zombie.images['Walk'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 100, 100)
            else:
                if self.speed == 0:
                    Zombie.images['Idle'][int(self.frame)].draw(self.x, self.y, 100, 100)
                else:
                    Zombie.images['Walk'][int(self.frame)].draw(self.x, self.y, 100, 100)
            draw_rectangle(*self.get_bb())
            self.font.draw(self.x - 50, self.y + 50, '(HP: %d)' % self.HP, (255, 255, 255))

    def handle_event(self, event):
        pass
