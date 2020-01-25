import os
from random import randint
import time
import numpy as np
from threading import Thread, Lock
import time
from getkey import getkey, keys

DINOSAUR_ASCII = "                __\n               / _)\n     _.----._/ /\n    /         /\n __/ (  | (  |\n/__.-|_|--|_|"
DINOSAUR_JUMPING_ASCII = "                __\n               / _)\n     _.----._/ /\n __/ (  | (  |\n/__.-|_|--|_|\n             "
DINOSAUR_DEAD_ASCII = "       __\n      /xx\\\n     |    |\n ^^  (vvvv)   ^^\n \\\\  /\__/\  //\n  \\\\/      \//\n   /        \        \n  |          |    ^  \n  /          \___/ | \n (            )     |\n  \----------/     /\n    //    \\\\_____/\n   W       W\n\n   GAME OVER\n"
GROUND_1_ASCII = "__._.__.__._"
GROUND_2_ASCII = "__...._.._._"
TREE_ASCII = "TTTTTTTTTTTT"
DINOSAUR = "d"
DINOSAUR_JUMPING = "j"
GROUND_1 = "g1"
GROUND_2 = "g2"
TREE = "t"
GRAPHIC_MAPPER = {
    DINOSAUR: DINOSAUR_ASCII,
    GROUND_1: GROUND_1_ASCII,
    GROUND_2: GROUND_2_ASCII,
    TREE: TREE_ASCII,
    DINOSAUR_JUMPING: DINOSAUR_JUMPING_ASCII
}
GROUND_COLLECTION = [GROUND_1, GROUND_2]
ENV_SIZE = 10
JUMP_FRAMES = 3

is_jumping = False
is_alive = True
jump_frames = 0

def run():
    global is_alive
    env = initialize_environment()
    score = 0
    while is_alive:
        clear_console()
        env = check_jump(env)
        if collision(env):
            is_alive = False
            clear_console()
            print(DINOSAUR_DEAD_ASCII)
            print(f"Final Score: {score}\n\nPress any key to exit.")
            return 0
        score += 1
        env = shift(env)
        print_game(score, env)
        time.sleep(0.3)

def print_game(score, environment):
    frame = f"Score: {score}\n"
    for cell in environment:
        frame += GRAPHIC_MAPPER[cell]
    print(frame)

def initialize_environment():
    return [DINOSAUR] + [np.random.choice(GROUND_COLLECTION) for x in range(ENV_SIZE-1)]

def clear_console():
    os.system('cls' if os.name=='nt' else 'clear')

def check_jump(env):
    global is_jumping
    global jump_frames
    global is_jumping
    jump_frames = jump_frames - 1
    if is_jumping:
        env[0] = DINOSAUR_JUMPING
        jump_frames = JUMP_FRAMES
        is_jumping = False
    if jump_frames == 0:
        env[0] = DINOSAUR
    return env

def shift(env):
    dino_current = env[0]
    env = [x for x in env[1:]] + [np.nan]
    env[0] = dino_current
    r = np.random.random_sample()
    if r > 0.75:
        env[-1] = TREE
    else:
        env[-1] = np.random.choice(GROUND_COLLECTION)
    return env

def collision(env):
    return env[1] == TREE and env[0] != DINOSAUR_JUMPING

def user_input():
    global is_jumping
    global is_alive
    global jump_frames
    while is_alive:
        if getkey(True) == keys.SPACE and jump_frames <= 0:
            is_jumping = True

thread1 = Thread(target=user_input)
thread2 = Thread(target=run)

thread1.start()
thread2.start()

thread1.join()
thread2.join()
