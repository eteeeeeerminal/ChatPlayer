# -*- coding: utf-8 -*-

# PyGameで配信に映すやつをつくる

import pygame
from pygame.locals import *
import sys
import time
import concurrent.futures

from ChatGetter import Chat_getter
from ChatPlayer import Chat_player

import json
import logging
import traceback

setting  = json.load(open("setting.json", 'r'))

DISPLAY_SIZE = tuple(setting["win_size"])
BACK_COLOR   = tuple(setting["back_color"])
URL          = setting["chat_url"]
GET_PERIOD   = setting["chat_get_period"]

print("complete loding json")
try:
    getter = Chat_getter(URL, driver_path=setting["chromedriver_path"])
except:
    getter.quit()
    sys.exit()
    
player = None

print("boot chrome_driver")

def main():
    global player, getter

    pygame.init()
    screen = pygame.display.set_mode(DISPLAY_SIZE)
    pygame.display.set_caption("ChatPlayer")
    clock = pygame.time.Clock()

    try:
        player = Chat_player(DISPLAY_SIZE)

    except:
        print("Error ChatPlayer")
        pygame.quit()
        getter.quit()
        sys.exit()

    def loop():
        clock.tick(30)
        screen.fill(BACK_COLOR)

        chat_renders = player.draw()
        if (not chat_renders == None) and (not chat_renders == []):
            [screen.blit(chat_render["chat"], chat_render["pos"]) for chat_render in chat_renders]

        pygame.display.update()
        
        # 終了処理
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                getter.quit()
                sys.exit()

    try:
        while True:
            loop()

    except:
        traceback.print_exc()
        pygame.quit()
        getter.quit()
        sys.exit()


def command_get():
    global getter, player
    while True:
        [player.command_process(c) for c in getter.get_chats()]
        time.sleep(GET_PERIOD)

executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
try:
    executor.submit(command_get)
    executor.submit(main)

except:
    getter.quit()
    sys.exit()