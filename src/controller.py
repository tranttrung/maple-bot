import pydirectinput
import time
import random
import json

class Controller:
    def __init__(self, config_path="src/config.json"):
        with open(config_path, "r") as f:
            self.config = json.load(f)
        
        # pydirectinput has a built in pause, we can turn it off and handle delays ourselves
        pydirectinput.PAUSE = 0.0

    def get_key(self, action_name):
        return self.config["key_bindings"].get(action_name)

    def sleep_random(self):
        delay = random.uniform(
            self.config["delays"]["min_random_delay"],
            self.config["delays"]["max_random_delay"]
        )
        time.sleep(delay)

    def press_key(self, key, duration=0.05):
        if not key:
            return
        pydirectinput.keyDown(key)
        time.sleep(duration + random.uniform(0.01, 0.05))
        pydirectinput.keyUp(key)
        self.sleep_random()

    def attack(self):
        key = self.get_key("attack")
        self.press_key(key, duration=0.05)

    def jump(self):
        key = self.get_key("jump")
        self.press_key(key, duration=0.05)

    def buff_1(self):
        key = self.get_key("buff_1")
        self.press_key(key, duration=0.2)
        print("Used Buff 1")

    def potion_hp(self):
        key = self.get_key("potion_hp")
        self.press_key(key, duration=0.1)
        print("Used HP Potion")

    def potion_mp(self):
        key = self.get_key("potion_mp")
        self.press_key(key, duration=0.1)
        print("Used MP Potion")

    def walk_left(self, duration):
        key = self.get_key("move_left")
        pydirectinput.keyDown(key)
        time.sleep(duration)
        pydirectinput.keyUp(key)
        self.sleep_random()

    def walk_right(self, duration):
        key = self.get_key("move_right")
        pydirectinput.keyDown(key)
        time.sleep(duration)
        pydirectinput.keyUp(key)
        self.sleep_random()

    def climb_ladder(self, duration=2.0):
        """
        Trèo thang: Nhấn giữ phím Up (mũi tên lên) đồng thời nhấn Space (nhảy) để bắt thang,
        sau đó giữ phím Up để leo lên.
        """
        up_key = self.get_key("move_up")
        jump_key = self.get_key("jump")
        
        # Nhấn Space + Up đồng thời để bắt thang
        pydirectinput.keyDown(up_key)
        time.sleep(0.05)
        pydirectinput.keyDown(jump_key)
        time.sleep(0.1)
        pydirectinput.keyUp(jump_key)
        
        # Giữ phím Up để leo lên trong khoảng thời gian cho trước
        time.sleep(duration)
        pydirectinput.keyUp(up_key)
        self.sleep_random()
        print("Climbed ladder")

    def drop_down(self):
        """
        Rớt xuống tầng dưới: Nhấn phím Down + Space để nhảy xuyên qua sàn.
        """
        down_key = self.get_key("move_down")
        jump_key = self.get_key("jump")
        
        pydirectinput.keyDown(down_key)
        time.sleep(0.05)
        pydirectinput.keyDown(jump_key)
        time.sleep(0.1)
        pydirectinput.keyUp(jump_key)
        time.sleep(0.1)
        pydirectinput.keyUp(down_key)
        self.sleep_random()
        print("Dropped down")
