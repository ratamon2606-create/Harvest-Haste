import pygame
import sys
import time
import math
import random
import csv
import os
from datetime import datetime
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import matplotlib.pyplot as plt
import logging

logging.getLogger('matplotlib.font_manager').disabled = True

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.init()


WIDTH, HEIGHT = 1024, 720
FPS = 60

IMAGE_PATHS = {
    "background": "asset/bg.png", "shop_building": "asset/shop.png", "house_building": "asset/house.png",
    "pond": "asset/pond.png", "fence": "asset/fence.png", "sign": "asset/sign.png", 
    "field_rice_empty": "asset/ricefield.png", "field_cabbage_empty": "asset/cabbagegarden.png",
    "crop_rice_ready": "asset/rice.png", "crop_cabbage_ready": "asset/cabbage.png",
    "cow_in_pen": "asset/cow.png", "inventory_bar": "asset/inventory.png", "shop_window": "asset/shopwindow.png",
    "bubble_seed": "asset/seedingbubble.png", "bubble_cab_seed": "asset/cabseedbubble.png",  
    "bubble_harvest": "asset/croppingbubble.png", "bubble_pick": "asset/pickbubble.png",         
    "bubble_fishing": "asset/fishingbubble.png", "bubble_kill": "asset/killbubble.png",         
    "bubble_cow": "asset/cowbubble.png", "icon_rice_seed": "asset/seedicon.png",
    "icon_cabbage_seed": "asset/cabbageseedicon.png", "icon_rice": "asset/riceicon.png",
    "icon_cabbage": "asset/cabbageicon.png", "icon_fish": "asset/fishicon.png",
    "icon_beef": "asset/beef.png", "icon_cow": "asset/c.png", "money": "asset/money.png",
    "kitchen": "asset/kitchen.png", "board": "asset/board.png", "pan": "asset/pan.png", "pot": "asset/pot.png",
    "knife": "asset/knife.png", "potspatula": "asset/potspatula.png", "panspatula": "asset/panspatula.png",
    "boardcabbage": "asset/boardcabbage.png", "cutcabbage": "asset/cutcabbage.png",
    "boardfish": "asset/boardfish.png", "cutfish": "asset/cutfish.png",
    "potcabbage": "asset/potcabbage.png", "potrice": "asset/potrice.png",
    "rawbeef": "asset/rawbeef.png", "cookedbeef": "asset/cookedbeef.png", "burntbeef": "asset/burntbeef.png",
    "rawfish": "asset/rawfish.png", "cookedfish": "asset/cookedfish.png", "burntfish": "asset/burntfish.png",
    "bowl": "asset/bowl.png", "soup": "asset/soup.png", "steak": "asset/steak.png",
    "ricefish": "asset/ricefish.png", "ricebeef": "asset/ricebeef.png", "saucefish": "asset/saucefish.png",
    "success": "asset/success.png", "fail": "asset/fail.png", "return_btn": "asset/returnbutton.png",
    "title_bg": "asset/harvestnhaste.png" 
}

HITBOXES = {
    "shop": pygame.Rect(400, 50, 150, 120),    
    "house": pygame.Rect(650, 20, 250, 200),   
    "field_1": pygame.Rect(320, 300, 150, 200), 
    "field_2": pygame.Rect(500, 300, 150, 200), 
    "cow_pen": pygame.Rect(700, 300, 150, 200), 
    "pond": pygame.Rect(60, 400, 220, 220),     
}

SHOP_ITEMS = {
    "close_btn": {"rect": pygame.Rect(200, 190, 50, 50), "type": "close"},
    "buy_rice":    {"rect": pygame.Rect(250, 245, 200, 60), "type": "buy", "item": "rice", "price": 16, "name": "Rice", "text_pos": (370, 245)},
    "buy_cabbage": {"rect": pygame.Rect(250, 327, 200, 60), "type": "buy", "item": "cabbage", "price": 10, "name": "Cabbage", "text_pos": (370, 327)},
    "buy_fish":    {"rect": pygame.Rect(250, 410, 200, 60), "type": "buy", "item": "fish", "price": 24, "name": "Fish", "text_pos": (370, 410)},
    "buy_beef":    {"rect": pygame.Rect(250, 495, 200, 60), "type": "buy", "item": "beef", "price": 40, "name": "Beef", "text_pos": (370, 495)},
    "buy_rice_seed": {"rect": pygame.Rect(530, 245, 200, 60), "type": "buy", "item": "rice_seed", "price": 5, "name": "Rice Seed", "text_pos": (650, 245)},
    "buy_cab_seed":  {"rect": pygame.Rect(530, 325, 200, 60), "type": "buy", "item": "cabbage_seed", "price": 5, "name": "Cab Seed", "text_pos": (650, 325)},
    "buy_cow":       {"rect": pygame.Rect(530, 405, 200, 60), "type": "buy", "item": "cow", "price": 20, "name": "Cow", "text_pos": (650, 405)},
}

TEXT_POS = {
    "rice": (125, 678), "cabbage": (183, 678), "fish": (250, 678),         
    "rice_seed": (312, 678), "cabbage_seed": (382, 678), 
    "beef": (450, 678), "cow": (510, 678), "money": (735, 645)         
}

SIGN_TEXT_X = 153
SIGN_TEXT_Y = 100

def get_image(key, size=None):
    path = IMAGE_PATHS.get(key, "")
    try:
        img = pygame.image.load(path).convert_alpha()
        if size:
            return pygame.transform.scale(img, size)
        return pygame.transform.scale(img, (WIDTH, HEIGHT)) 
    except FileNotFoundError:
        surf = pygame.Surface(size if size else (WIDTH, HEIGHT), pygame.SRCALPHA)
        surf.fill((150, 150, 150, 128))
        return surf


class DataTracker:
    def __init__(self):
        self.main_file = "all_gameplay_stats.csv"        
        self.session_file = "current_session_stats.csv"  
        self.headers = ["Timestamp", "EventType", "Level", "Item", "Value1", "Value2"]
        self.records = []
        
        if not os.path.exists(self.main_file):
            with open(self.main_file, mode='w', newline='', encoding='utf-8') as f:
                csv.writer(f).writerow(self.headers)
                
        with open(self.session_file, mode='w', newline='', encoding='utf-8') as f:
            csv.writer(f).writerow(self.headers)

    def log(self, event_type, level, item="", val1="", val2=""):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.records.append([timestamp, event_type, level, item, val1, val2])

    def save_to_csv(self):
        if not self.records: return
        with open(self.main_file, mode='a', newline='', encoding='utf-8') as f:
            csv.writer(f).writerows(self.records)
        with open(self.session_file, mode='a', newline='', encoding='utf-8') as f:
            csv.writer(f).writerows(self.records)
        self.records = [] 


class FarmEntity:
    def __init__(self):
        self.growthState = "EMPTY"
        self.timeToProduce = 0
        self.isReady = False

    def updateState(self, dt=0): pass
    def interactToHarvest(self, inventory): return False

class Ingredient:
    def __init__(self, name, state):
        self.itemName = name
        self.currentState = state

class CookingStation:
    def __init__(self):
        self.isOccupied = False
        self.currentItem = None
        self.processingTimer = 0.0
        self.tracker = None
        self.level = 1

    def set_context(self, tracker, level):
        self.tracker = tracker
        self.level = level

    def placeItem(self, ingredient: Ingredient):
        self.currentItem = ingredient
        self.isOccupied = True

    def retrieveItem(self):
        item = self.currentItem
        self.currentItem = None
        self.isOccupied = False
        return item

class CuttingBoard(CookingStation):
    def chop(self): pass

class Stove(CookingStation):
    def __init__(self):
        super().__init__()
        self.isBurning = False
    def boilOrFry(self, dt): pass

class OrderManager:
    def __init__(self):
        self.activeOrders = []
        self.timeLimit = 0
    def generateOrder(self): pass
    def checkDishCompletion(self): pass


class Animal(FarmEntity):
    def __init__(self, bounds_rect):
        super().__init__()
        self.hungerLevel = 0 
        self.bounds = bounds_rect
        self.cow_w = 64
        self.cow_h = 82
        self.min_x = self.bounds.left + 10
        self.max_x = self.bounds.right - self.cow_w - 10
        self.min_y = self.bounds.top + 10
        self.max_y = self.bounds.bottom - self.cow_h - 10
        self.x = random.uniform(self.min_x, self.max_x)
        self.y = random.uniform(self.min_y, self.max_y)
        self.target_x = self.x
        self.target_y = self.y
        self.state = "PAUSED"
        self.growthState = self.state
        self.pause_timer = random.uniform(1.0, 3.0)
        self.speed = 25.0 

    def feedAnimal(self): self.hungerLevel = 0

    def wander(self, dt):
        if self.state == "PAUSED":
            self.pause_timer -= dt
            if self.pause_timer <= 0:
                self.target_x = random.uniform(self.min_x, self.max_x)
                self.target_y = random.uniform(self.min_y, self.max_y)
                self.state = "MOVING"
        elif self.state == "MOVING":
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            dist = math.hypot(dx, dy)
            if dist < 5.0:
                self.x = self.target_x
                self.y = self.target_y
                self.state = "PAUSED"
                self.pause_timer = random.uniform(2.0, 5.0)
            else:
                move_dist = self.speed * dt
                if move_dist > dist: move_dist = dist
                self.x += (dx / dist) * move_dist
                self.y += (dy / dist) * move_dist
        self.growthState = self.state

    def updateState(self, dt): self.wander(dt)
    def update(self, dt): self.updateState(dt)
    def draw(self, screen, sprite): screen.blit(sprite, (self.x, self.y))


class Crop(FarmEntity):
    def __init__(self, hitbox, crop_type, empty_img_key, seed_bubble_key, harvest_bubble_key, grow_duration=3):
        super().__init__()
        self.waterLevel = 100 
        self.hitbox = hitbox
        self.crop_type = crop_type 
        self.empty_img_key = empty_img_key 
        self.seed_bubble_key = seed_bubble_key
        self.harvest_bubble_key = harvest_bubble_key 
        self.state = "EMPTY" 
        self.plant_time = 0
        self.grow_duration = grow_duration 
        self.timeToProduce = self.grow_duration

    def waterCrop(self): self.waterLevel = 100

    def updateState(self):
        if self.state == "SEEDED" and time.time() - self.plant_time > self.grow_duration:
            self.state = "READY"
            self.isReady = True
        self.growthState = self.state

    def interactToHarvest(self, inventory):
        if self.state == "EMPTY":
            req_seed = f"{self.crop_type}_seed"
            if inventory.get(req_seed, 0) > 0:
                inventory[req_seed] -= 1
                self.state = "SEEDED"
                self.growthState = "SEEDED"
                self.plant_time = time.time()
                return True
        elif self.state == "READY":
            inventory[self.crop_type] += 1
            self.state = "EMPTY"
            self.growthState = "EMPTY"
            self.isReady = False
            return True
        return False
        
    def update(self): self.updateState()
    def handle_click(self, inventory): return self.interactToHarvest(inventory)


class SlicingStep(CuttingBoard):
    def __init__(self, target_swipes, start_img_key, end_img_key):
        super().__init__()
        self.placeItem(Ingredient("Veg/Meat", "Raw"))
        self.station = "Cutting Board"
        self.target_swipes = target_swipes
        self.current_swipes = 0
        self.bg_sprite = get_image("board") 
        self.start_sprite = get_image(start_img_key)
        self.end_sprite = get_image(end_img_key)
        try:
            self.knife_sprite = pygame.image.load(IMAGE_PATHS["knife"]).convert_alpha()
        except FileNotFoundError:
            self.knife_sprite = get_image("knife") 
        self.completed = False
        self.completion_timer = 0.5 
        self.tilt_timer = 0.0

    def chop(self):
        if not self.completed:
            self.current_swipes += 1
            self.tilt_timer = 0.1
            if self.current_swipes >= self.target_swipes:
                self.completed = True
                self.currentItem.currentState = "Chopped"

    def update(self, dt):
        if self.tilt_timer > 0:
            self.tilt_timer -= dt
        if self.completed: self.completion_timer -= dt

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN: self.chop()

    def draw(self, screen, font, mouse_pos=None):
        screen.blit(self.bg_sprite, (0, 0))
        if self.completed:
            screen.blit(self.end_sprite, (0, 0))
        else:
            screen.blit(self.start_sprite, (0, 0))
            if mouse_pos is None: mouse_pos = pygame.mouse.get_pos()
            
            angle = 40 if self.tilt_timer > 0 else 0
            rotated_knife = pygame.transform.rotate(self.knife_sprite, angle)
            knife_rect = rotated_knife.get_rect()
            knife_rect.center = mouse_pos
            screen.blit(rotated_knife, knife_rect) 
            
            text = font.render(f"Click to Chop! ({self.current_swipes}/{self.target_swipes})", True, (0,0,0))
            screen.blit(text, (WIDTH//2 - text.get_width()//2, 100))

    def is_completed(self): return self.completed and self.completion_timer <= 0
    def is_failed(self): return False


class BoilingStep(Stove):
    def __init__(self, required_time=5.0, ingredient_img_key=None):
        super().__init__()
        self.placeItem(Ingredient("Broth", "Raw"))
        self.station = "Pot"
        self.required_time = required_time
        self.current_time_in_zone = 0.0
        self.heat_level = 50.0 
        self.spatula_offset_x = 0 
        self.pot_sprite = get_image("pot")
        self.ingredient_sprite = get_image(ingredient_img_key) if ingredient_img_key else None
        self.spatula_sprite = get_image("potspatula") 
        
        self.drift_direction = random.choice([-1, 1])
        self.drift_timer = random.uniform(0.5, 1.5)
        self.drift_speed = random.uniform(20.0, 40.0)

    def boilOrFry(self, dt):
        self.drift_timer -= dt
        if self.drift_timer <= 0:
            self.drift_direction = random.choice([-1, 1])
            self.drift_timer = random.uniform(0.5, 1.5)
            self.drift_speed = random.uniform(20.0, 40.0)

        self.heat_level += self.drift_direction * self.drift_speed * dt
        self.heat_level = max(0, min(100, self.heat_level))
        
        if 35 <= self.heat_level <= 65:
            self.current_time_in_zone += dt
        self.spatula_offset_x *= 0.9 

    def update(self, dt): self.boilOrFry(dt)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.heat_level -= 10
                self.spatula_offset_x = -80
            elif event.key == pygame.K_RIGHT:
                self.heat_level += 10
                self.spatula_offset_x = 80

    def draw(self, screen, font, mouse_pos=None):
        screen.blit(self.pot_sprite, (0, 0))
        if self.ingredient_sprite: screen.blit(self.ingredient_sprite, (0, 0))
        screen.blit(self.spatula_sprite, (self.spatula_offset_x - 50, 0))
        gauge_rect = pygame.Rect(WIDTH//2 - 150, 150, 300, 30)
        pygame.draw.rect(screen, (100, 100, 100), gauge_rect)
        green_rect = pygame.Rect(WIDTH//2 - 150 + 105, 150, 90, 30)
        pygame.draw.rect(screen, (0, 255, 0), green_rect)
        indicator_x = (WIDTH//2 - 150) + (self.heat_level / 100.0) * 300
        pygame.draw.line(screen, (255, 0, 0), (indicator_x, 140), (indicator_x, 190), 5)
        prog_text = font.render(f"Press <- LEFT and RIGHT -> to stay green! {self.current_time_in_zone:.1f}/{self.required_time}s", True, (0,0,0))
        screen.blit(prog_text, (WIDTH//2 - prog_text.get_width()//2, 100))

    def is_completed(self): return self.current_time_in_zone >= self.required_time
    def is_failed(self): return False


class GrillingStep(Stove):
    def __init__(self, raw_img_key, cooked_img_key, burnt_img_key):
        super().__init__()
        self.placeItem(Ingredient("Meat/Fish", "Raw"))
        self.station = "Pan"
        self.pan_sprite = get_image("pan")
        self.raw_sprite = get_image(raw_img_key)
        self.cooked_sprite = get_image(cooked_img_key)
        self.burnt_sprite = get_image(burnt_img_key)
        self.spatula_sprite = get_image("panspatula")
        self.spatula_offset_x = 0
        self.hits = 0
        self.target_hits = 5
        self.timer = 0.0
        self.time_limit = 15.0
        self.gauge_start_x = WIDTH//2 - 150
        self.gauge_width = 300
        self.indicator_x = 0
        self.indicator_dir = 1
        self.indicator_speed = 350 
        self.randomize_green_zone()
        self.state = "PLAYING" 
        self.end_timer = 1.5 

    def randomize_green_zone(self):
        self.green_width = random.randint(40, 70)
        self.green_x = random.randint(0, self.gauge_width - self.green_width)

    def boilOrFry(self, dt):
        if self.state == "PLAYING":
            self.timer += dt
            self.indicator_x += self.indicator_speed * self.indicator_dir * dt
            if self.indicator_x <= 0:
                self.indicator_x = 0
                self.indicator_dir = 1
            elif self.indicator_x >= self.gauge_width:
                self.indicator_x = self.gauge_width
                self.indicator_dir = -1
            if self.timer >= self.time_limit:
                self.state = "BURNT"
                self.isBurning = True
                self.currentItem.currentState = "Burnt"
                if self.tracker:
                    self.tracker.log("Waste_Event", self.level, self.station)
        else:
            self.end_timer -= dt
        self.spatula_offset_x *= 0.8 

    def update(self, dt): self.boilOrFry(dt)

    def handle_event(self, event):
        if self.state == "PLAYING" and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.spatula_offset_x = -50 
            if self.green_x <= self.indicator_x <= self.green_x + self.green_width:
                self.hits += 1
                if self.hits >= self.target_hits:
                    self.state = "COOKED" 
                    self.currentItem.currentState = "Cooked"
                else:
                    self.randomize_green_zone()

    def draw(self, screen, font, mouse_pos=None):
        screen.blit(self.pan_sprite, (0, 0))
        if self.state == "PLAYING": screen.blit(self.raw_sprite, (0, 0))
        elif self.state == "COOKED": screen.blit(self.cooked_sprite, (0, 0))
        elif self.state == "BURNT": screen.blit(self.burnt_sprite, (0, 0))
        screen.blit(self.spatula_sprite, (self.spatula_offset_x - 50, 0))
        if self.state == "PLAYING":
            g_rect = pygame.Rect(self.gauge_start_x, 150, self.gauge_width, 30)
            pygame.draw.rect(screen, (100, 100, 100), g_rect)
            green_rect = pygame.Rect(self.gauge_start_x + self.green_x, 150, self.green_width, 30)
            pygame.draw.rect(screen, (0, 255, 0), green_rect)
            indicator_pos = self.gauge_start_x + self.indicator_x
            pygame.draw.line(screen, (255, 0, 0), (indicator_pos, 140), (indicator_pos, 190), 5)
            time_left = max(0, self.time_limit - self.timer)
            text = font.render(f"Spacebar to Hit! ({self.hits}/{self.target_hits})  Time: {time_left:.1f}s", True, (0,0,0))
            screen.blit(text, (WIDTH//2 - text.get_width()//2, 100))

    def is_completed(self): return self.state == "COOKED" and self.end_timer <= 0
    def is_failed(self): return self.state == "BURNT" and self.end_timer <= 0


class MinigameManager(OrderManager):
    def __init__(self, level, recipe_steps, time_limit, reveal_keys, reward_amount, penalty_ingredients, tracker):
        super().__init__()
        self.level = level
        self.tracker = tracker
        self.steps = recipe_steps
        self.current_step_index = 0
        for step in self.steps:
            if hasattr(step, 'set_context'): step.set_context(self.tracker, self.level)
        self.time_limit = time_limit
        self.timeLimit = time_limit
        self.time_remaining = time_limit
        self.reveal_keys = reveal_keys 
        self.reward_amount = reward_amount
        self.penalty_ingredients = penalty_ingredients 
        self.activeOrders = [penalty_ingredients] 
        self.state = "PLAYING" 
        self.reveal_timer = 3.0 
        self.step_timer = 0.0
        self.bg = get_image("kitchen")
        self.success_img = get_image("success")
        self.fail_img = get_image("fail")
        self.return_btn = get_image("return_btn")

    def generateOrder(self): pass

    def checkDishCompletion(self, current_step):
        if current_step.is_failed():
            self.state = "FAIL"
            pygame.mouse.set_visible(True)
            return False
        if current_step.is_completed():
            self.current_step_index += 1
            self.step_timer = 0.0
            if self.current_step_index >= len(self.steps):
                self.state = "DISH_REVEAL" 
                pygame.mouse.set_visible(True)
        return True

    def update(self, dt):
        if self.state == "PLAYING":
            self.time_remaining -= dt
            self.step_timer += dt
            if self.time_remaining <= 0:
                self.state = "FAIL"
                pygame.mouse.set_visible(True)
                return
            current_step = self.steps[self.current_step_index]
            current_step.update(dt)
            self.checkDishCompletion(current_step)
        elif self.state == "DISH_REVEAL":
            self.reveal_timer -= dt
            if self.reveal_timer <= 0: self.state = "SUCCESS" 

    def handle_event(self, event):
        if self.state == "PLAYING": self.steps[self.current_step_index].handle_event(event)
        elif self.state in ["SUCCESS", "FAIL"] and event.type == pygame.MOUSEBUTTONDOWN: return self.state 
        return None

    def draw(self, screen, font, mouse_pos=None):
        screen.blit(self.bg, (0, 0))
        if self.state == "PLAYING":
            timer_text = font.render(f"Overall Time: {max(0, self.time_remaining):.1f}s", True, (255, 0, 0))
            screen.blit(timer_text, (20, 20))
            self.steps[self.current_step_index].draw(screen, font, mouse_pos)
        elif self.state == "DISH_REVEAL":
            for key in self.reveal_keys: screen.blit(get_image(key), (0, 0))
            text = font.render("Dish Completed!", True, (0, 0, 0))
            screen.blit(text, (WIDTH//2 - text.get_width()//2, 100))
        elif self.state == "SUCCESS":
            for key in self.reveal_keys: screen.blit(get_image(key), (0, 0))
            screen.blit(self.success_img, (0, 0)) 
            screen.blit(self.return_btn, (0, 0))
            try: large_font = pygame.font.Font("asset/Dudu_Calligraphy.ttf", 60)
            except: large_font = pygame.font.SysFont(None, 60)
            success_main_txt = large_font.render("SUCCESS!", True, (34, 139, 34))
            screen.blit(success_main_txt, (WIDTH//2 - success_main_txt.get_width()//2, HEIGHT//2 - 60))
            reward_txt = font.render(f"Reward: +{self.reward_amount}$", True, (34, 139, 34))
            screen.blit(reward_txt, (WIDTH//2 - reward_txt.get_width()//2, HEIGHT//2 + 30))
        elif self.state == "FAIL":
            screen.blit(self.fail_img, (0, 0))
            screen.blit(self.return_btn, (0, 0))
            try: large_font = pygame.font.Font("asset/Dudu_Calligraphy.ttf", 60)
            except: large_font = pygame.font.SysFont(None, 60)
            fail_main_txt = large_font.render("FAILED!", True, (200, 0, 0))
            screen.blit(fail_main_txt, (WIDTH//2 - fail_main_txt.get_width()//2, HEIGHT//2 - 60))
            lost_text = ", ".join([ing.capitalize() for ing in self.penalty_ingredients])
            penalty_txt = font.render(f"Lost: {lost_text}", True, (200, 0, 0))
            screen.blit(penalty_txt, (WIDTH//2 - penalty_txt.get_width()//2, HEIGHT//2 + 30))


class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        self.internal_screen = pygame.Surface((WIDTH, HEIGHT))
        pygame.display.set_caption("Harvest & Haste")
        
        self.current_music = None 
        
        self.clock = pygame.time.Clock()
        try: self.font = pygame.font.Font("asset/Dudu_Calligraphy.ttf", 30)  
        except: self.font = pygame.font.SysFont(None, 30) 
        self.tracker = DataTracker()
        self.game_state = "START_MENU" 
        self.start_button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT - 150, 200, 60)
        self.minigame = None
        self.current_level = 1
        self.money = 5
        self.level_start_money = self.money 
        self.inventory = {"rice": 0, "cabbage": 0, "fish": 0, "rice_seed": 0, "cabbage_seed": 0, "beef": 0, "cow": 0}
        self.level_requirements = {
            1: {"cabbage": 1}, 2: {"beef": 1, "cabbage": 2}, 3: {"fish": 2, "rice": 2},
            4: {"beef": 2, "rice": 2, "cabbage": 1}, 5: {"fish": 2, "cabbage": 2, "rice": 2, "beef": 2}
        }
        self.show_shop = False
        self.tutorial_first_seed_bought = False
        self.shop_msg = ""
        self.shop_msg_timer = 0.0
        self.assets = {key: get_image(key) for key in IMAGE_PATHS}
        self.cow_sprite = get_image("cow_in_pen", (80, 80))
        self.wandering_cows = [] 
        self.last_fish_time = time.time() 
        self.cow_placed_time = 0
        self.field_rice = Crop(HITBOXES["field_1"], "rice", "field_rice_empty", "bubble_seed", "bubble_harvest", 10)
        self.field_cabbage = Crop(HITBOXES["field_2"], "cabbage", "field_cabbage_empty", "bubble_cab_seed", "bubble_pick", 5)
        self.fields = [self.field_rice, self.field_cabbage]
        self.cows_in_pen = 0

    def play_music(self, track_name, loops=-1):
        if self.current_music != track_name:
            self.current_music = track_name
            try:
                pygame.mixer.music.load(f"asset/{track_name}.mp3")
                pygame.mixer.music.play(loops)
            except Exception as e:
                pass

    def get_scaled_mouse_pos(self, raw_pos):
        win_w, win_h = self.window.get_size()
        scale = min(win_w / WIDTH, win_h / HEIGHT)
        offset_x = (win_w - WIDTH * scale) / 2
        offset_y = (win_h - HEIGHT * scale) / 2
        return int((raw_pos[0] - offset_x) / scale), int((raw_pos[1] - offset_y) / scale)

    def draw_text(self, text, pos, color=(0, 0, 0)):
        txt_surf = self.font.render(str(text), True, color)
        self.internal_screen.blit(txt_surf, pos)

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            
            if self.game_state == "START_MENU":
                self.run_start_menu_logic(dt)
            elif self.game_state == "FARM": 
                self.run_farm_logic(dt)
            elif self.game_state == "COOKING": 
                self.run_cooking_logic(dt)
            
            win_w, win_h = self.window.get_size()
            scale = min(win_w / WIDTH, win_h / HEIGHT)
            scaled_w = int(WIDTH * scale)
            scaled_h = int(HEIGHT * scale)
            
            scaled_screen = pygame.transform.scale(self.internal_screen, (scaled_w, scaled_h))
            
            offset_x = (win_w - scaled_w) // 2
            offset_y = (win_h - scaled_h) // 2
            
            self.window.fill((0, 0, 0)) 
            self.window.blit(scaled_screen, (offset_x, offset_y))
            pygame.display.flip()

    def exit_game(self):
        self.tracker.save_to_csv()
        pygame.display.quit()
        pygame.quit()
        self.show_dashboard()
        sys.exit()

    def run_start_menu_logic(self, dt):
        self.play_music("start") 
        
        self.internal_screen.blit(self.assets["title_bg"], (0, 0))
        
        mouse_pos = pygame.mouse.get_pos()
        scaled_mouse_pos = self.get_scaled_mouse_pos(mouse_pos)
        
        btn_color = (210, 180, 140) 
        if self.start_button_rect.collidepoint(scaled_mouse_pos):
            btn_color = (230, 200, 160) 
            
        pygame.draw.rect(self.internal_screen, btn_color, self.start_button_rect, border_radius=15)
        pygame.draw.rect(self.internal_screen, (62, 39, 35), self.start_button_rect, width=4, border_radius=15) 
        
        txt_surf = self.font.render("START GAME", True, (62, 39, 35))
        txt_rect = txt_surf.get_rect(center=self.start_button_rect.center)
        self.internal_screen.blit(txt_surf, txt_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.start_button_rect.collidepoint(scaled_mouse_pos):
                    self.tracker.log("Interaction", self.current_level, "Start_Game")
                    self.game_state = "FARM"

    def run_farm_logic(self, dt):
        self.play_music("farm")
        
        self.internal_screen.blit(self.assets["background"], (0, 0))
        self.internal_screen.blit(self.assets["pond"], (0, 0))
        self.internal_screen.blit(self.assets["fence"], (0, 0))
        self.internal_screen.blit(self.assets["sign"], (0, 0)) 
        self.internal_screen.blit(self.assets["shop_building"], (0, 0))
        self.internal_screen.blit(self.assets["house_building"], (0, 0))
        self.draw_text(f"LEVEL {self.current_level}", (SIGN_TEXT_X, SIGN_TEXT_Y), color=(90, 50, 20))
        
        current_reqs = self.level_requirements.get(self.current_level, self.level_requirements[5])
        y_offset = SIGN_TEXT_Y + 40
        for item, count in current_reqs.items():
            self.draw_text(f"{item} x{count}", (SIGN_TEXT_X-5, y_offset), color=(90, 50, 20))
            y_offset += 30

        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.exit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                pos = self.get_scaled_mouse_pos(event.pos)
                self.tracker.log("Click_Position", self.current_level, "", pos[0], pos[1])
                
                if self.show_shop:
                    for key, data in SHOP_ITEMS.items():
                        if data["rect"].collidepoint(pos):
                            if data["type"] == "close":
                                self.tracker.log("Interaction", self.current_level, "Shop_Close")
                                self.show_shop = False
                            elif data["type"] == "buy":
                                if event.button == 1:
                                    if self.money >= data["price"]:
                                        self.tracker.log("Interaction", self.current_level, f"Buy_{data['item']}")
                                        self.money -= data["price"]
                                        self.inventory[data["item"]] += 1
                                        if data["item"] == "cabbage_seed":
                                            self.tutorial_first_seed_bought = True
                                elif event.button == 3:
                                    if self.inventory[data["item"]] > 0:
                                        self.tracker.log("Interaction", self.current_level, f"Sell_{data['item']}")
                                        self.inventory[data["item"]] -= 1
                                        self.money += data["price"]
                else:
                    if HITBOXES["shop"].collidepoint(pos):
                        self.tracker.log("Interaction", self.current_level, "Shop")
                        self.show_shop = True
                    elif HITBOXES["house"].collidepoint(pos):
                        self.tracker.log("Interaction", self.current_level, "House")
                        if all(self.inventory.get(ing, 0) >= qty for ing, qty in current_reqs.items()):
                            self.start_level_minigame(self.current_level, list(current_reqs.keys()))
                    elif HITBOXES["pond"].collidepoint(pos):
                        self.tracker.log("Interaction", self.current_level, "Pond")
                        if time.time() - self.last_fish_time > 15:
                            self.inventory["fish"] += 1
                            self.last_fish_time = time.time()
                    elif HITBOXES["cow_pen"].collidepoint(pos):
                        self.tracker.log("Interaction", self.current_level, "Cow_Pen")
                        if self.inventory["cow"] > 0 and self.cows_in_pen == 0:
                            self.inventory["cow"] -= 1; self.cows_in_pen += 1
                            self.wandering_cows.append(Animal(HITBOXES["cow_pen"]))
                            self.cow_placed_time = time.time()
                        elif self.cows_in_pen > 0 and (time.time() - self.cow_placed_time >= 20):
                            self.cows_in_pen -= 1; self.inventory["beef"] += 1
                            if self.wandering_cows: self.wandering_cows.pop()
                    else:
                        for field in self.fields:
                            if field.hitbox.collidepoint(pos):
                                self.tracker.log("Interaction", self.current_level, f"Field_{field.crop_type}")
                                old_state = field.state
                                success = field.handle_click(self.inventory)
                                if success and old_state == "READY":
                                    self.tracker.log("Harvest", self.current_level, field.crop_type)

        for field in self.fields:
            field.update()
            self.internal_screen.blit(self.assets[field.empty_img_key], (0, 0))
            if field.state == "READY":
                self.internal_screen.blit(self.assets[f"crop_{field.crop_type}_ready"], (0, 0))
                self.internal_screen.blit(self.assets[field.harvest_bubble_key], (0, 0))
            if field.state == "EMPTY": self.internal_screen.blit(self.assets[field.seed_bubble_key], (0, 0))

        if self.cows_in_pen > 0:
            for cow in self.wandering_cows:
                cow.update(dt)
                cow.draw(self.internal_screen, self.cow_sprite)
            if time.time() - self.cow_placed_time >= 20: 
                self.internal_screen.blit(self.assets["bubble_kill"], (0, 0))
        else: self.internal_screen.blit(self.assets["bubble_cow"], (0, 0))

        if time.time() - self.last_fish_time > 15: 
            self.internal_screen.blit(self.assets["bubble_fishing"], (0, 0))
        self.internal_screen.blit(self.assets["inventory_bar"], (0, 0))
        self.internal_screen.blit(self.assets["money"], (0, 0)) 
        
        for item in ["rice", "cabbage", "fish", "rice_seed", "cabbage_seed", "beef", "cow"]:
            if self.inventory[item] > 0:
                self.internal_screen.blit(self.assets[f"icon_{item}"], (0, 0))
                self.draw_text(self.inventory[item], TEXT_POS[item])
        self.draw_text(self.money, TEXT_POS["money"], color=(90, 50, 20))
        
        if self.show_shop:
            self.internal_screen.blit(self.assets["shop_window"], (0, 0))
            
            for key, data in SHOP_ITEMS.items():
                if data["type"] == "buy":
                    x, y = data["text_pos"]
                    self.draw_text(data["name"], (x, y), color=(120, 80, 50))
                    self.draw_text(f"$ {data['price']}", (x, y + 25), color=(200, 0, 0))
            
            self.draw_text("Left: buy", (WIDTH//2 + 45, 480), color=(119, 154, 104))
            self.draw_text("Right: sell", (WIDTH//2 + 45, 518), color=(119, 154, 104))
                
            if self.shop_msg_timer > 0:
                self.shop_msg_timer -= dt
                self.draw_text(self.shop_msg, (WIDTH//2, 550), color=(200, 0, 0))

    def start_level_minigame(self, level, req_list):
        pygame.mouse.set_visible(False)
        if level == 1:
            recipe = [SlicingStep(4, "boardcabbage", "cutcabbage"), BoilingStep(5.0, "potcabbage")]
            self.minigame = MinigameManager(level, recipe, 10.0, ["bowl", "soup"], 35, req_list, self.tracker)
        elif level == 2:
            recipe = [SlicingStep(5, "rawbeef", "rawbeef"), GrillingStep("rawbeef", "cookedbeef", "burntbeef"), SlicingStep(4, "boardcabbage", "cutcabbage"), BoilingStep(5.0, "potcabbage")]
            self.minigame = MinigameManager(level, recipe, 20.0, ["bowl", "steak"], 50, req_list, self.tracker)
        elif level == 3:
            recipe = [BoilingStep(5.0, "potrice"), SlicingStep(6, "boardfish", "cutfish"), GrillingStep("rawfish", "cookedfish", "burntfish"), SlicingStep(6, "boardfish", "cutfish"), GrillingStep("rawfish", "cookedfish", "burntfish")]
            self.minigame = MinigameManager(level, recipe, 30.0, ["bowl", "ricefish"], 65, req_list, self.tracker)
        elif level == 4:
            recipe = [BoilingStep(6.0, "potrice"), SlicingStep(6, "rawbeef", "rawbeef"), GrillingStep("rawbeef", "cookedbeef", "burntbeef"), SlicingStep(6, "rawbeef", "rawbeef"), GrillingStep("rawbeef", "cookedbeef", "burntbeef"), SlicingStep(5, "boardcabbage", "cutcabbage"), BoilingStep(5.0, "potcabbage")]
            self.minigame = MinigameManager(level, recipe, 35.0, ["bowl", "ricebeef"], 90, req_list, self.tracker)
        else: 
            recipe = [SlicingStep(8, "boardfish", "cutfish"), GrillingStep("rawfish", "cookedfish", "burntfish"), SlicingStep(8, "boardfish", "cutfish"), GrillingStep("rawfish", "cookedfish", "burntfish"), SlicingStep(6, "boardcabbage", "cutcabbage"), BoilingStep(6.0, "potrice"), SlicingStep(8, "rawbeef", "rawbeef"), GrillingStep("rawbeef", "cookedbeef", "burntbeef")]
            self.minigame = MinigameManager(level, recipe, 40.0, ["bowl", "saucefish"], 200, req_list, self.tracker)
        self.game_state = "COOKING"

    def run_cooking_logic(self, dt):
        if self.minigame.state == "PLAYING":
            self.play_music("kitchen")
        elif self.minigame.state == "DISH_REVEAL":
            pygame.mixer.music.stop()
            self.current_music = None 
        elif self.minigame.state == "SUCCESS":
            self.play_music("success", loops=0) 
        elif self.minigame.state == "FAIL":
            self.play_music("fail", loops=0) 
            
        self.minigame.update(dt)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.exit_game()
            result = self.minigame.handle_event(event)
            if result in ["SUCCESS", "FAIL"]:
                total_time = self.minigame.time_limit - self.minigame.time_remaining
                self.tracker.log("Level_Result", self.current_level, "", round(total_time, 2), result)
                
                if result == "SUCCESS":
                    for ing in self.minigame.penalty_ingredients: 
                        self.inventory[ing] -= self.level_requirements[self.current_level][ing] 
                    self.money += self.minigame.reward_amount 
                    self.tracker.save_to_csv()
                    
                    if self.current_level < 5:
                        self.current_level += 1 
                        self.level_start_money = self.money 
                        self.game_state = "FARM"
                        pygame.mouse.set_visible(True)
                    else:
                        pygame.mouse.set_visible(True)
                        self.exit_game()               
                elif result == "FAIL":
                    for ing in self.minigame.penalty_ingredients:
                        if self.inventory.get(ing, 0) > 0: 
                            qty_lost = self.level_requirements[self.current_level][ing]
                            self.inventory[ing] -= qty_lost
                            
                            for _ in range(qty_lost):
                                self.tracker.log("Waste_Event", self.current_level, ing)
                                
                    min_cost = 0
                    for req_item, count in self.level_requirements[self.current_level].items():
                        if req_item == "cabbage":
                            min_cost += count * 5
                        elif req_item == "rice":
                            min_cost += count * 5
                        elif req_item == "beef":
                            min_cost += count * 20
                            
                    self.money = min_cost
                    
                    self.game_state = "FARM"
                    pygame.mouse.set_visible(True)
                    self.tracker.save_to_csv()
        
        self.internal_screen.fill((255, 255, 255))
        scaled_mouse_pos = self.get_scaled_mouse_pos(pygame.mouse.get_pos())
        self.minigame.draw(self.internal_screen, self.font, scaled_mouse_pos)


    def show_dashboard(self):
        root = tk.Tk()
        root.title("Harvest & Haste Dashboard")
        root.geometry("1400x800") 

        try:
            df = pd.read_csv(self.tracker.session_file)
        except:
            df = pd.DataFrame()

        plt.rcdefaults() 
        plt.rcParams['lines.solid_capstyle'] = 'round'
        plt.rcParams['lines.solid_joinstyle'] = 'round'
        plt.rcParams['patch.edgecolor'] = '#3E2723' 
        plt.rcParams['patch.force_edgecolor'] = True
        plt.rcParams['lines.linewidth'] = 3.0
        plt.rcParams['patch.linewidth'] = 2.5 
        plt.rcParams['axes.linewidth'] = 2.5
        plt.rcParams['font.family'] = 'Comic Sans MS'
        
        P_BG_CREAM = '#FAF0E6'  
        P_TEXT_BROWN = '#3E2723' 
        P_TAN = '#D2B48C'        
        P_SIENNA = '#A0522D'     
        P_ARTICHOKE = '#8F9779'  
        P_TERRACOTTA = '#CD5C5C' 
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 10), facecolor=P_BG_CREAM)
        fig.suptitle("Your Gameplay Analytics", fontsize=22, fontweight='bold', color=P_TEXT_BROWN)

        def style_cute_ax(ax, title):
            ax.set_title(title, fontweight='bold', color=P_TEXT_BROWN, fontsize=14, pad=10)
            ax.set_facecolor(P_BG_CREAM)
            for spine in ax.spines.values():
                spine.set_color(P_TEXT_BROWN)
                spine.set_capstyle('round')
                spine.set_joinstyle('round')
            ax.tick_params(axis='both', colors=P_TEXT_BROWN, labelsize=10, width=2.5, length=6)


        level_results = df[df["EventType"] == "Level_Result"].copy()
        ax = axes[0, 0]
        style_cute_ax(ax, "Level Success Times (Stats)")
        ax.axis('tight')
        ax.axis('off')
        
        if not level_results.empty:
            level_results["Value1"] = pd.to_numeric(level_results["Value1"])
            success_times = level_results[level_results["Value2"] == "SUCCESS"]["Value1"]
            if not success_times.empty:
                stats = success_times.agg(['mean', 'median', 'min', 'max']).round(2).to_frame().reset_index()
                stats.columns = ['Metric', 'Seconds']
                table = ax.table(cellText=stats.values, colLabels=stats.columns, loc='center', cellLoc='center', bbox=[0.1, 0.1, 0.8, 0.8])
                
                for (row, col), cell in table.get_celld().items():
                    cell.set_edgecolor(P_TEXT_BROWN)
                    cell.set_linewidth(2)
                    if row == 0:
                        cell.set_facecolor(P_TAN)
                        cell.set_text_props(weight='bold', color=P_TEXT_BROWN, size=11)
                    else:
                        cell.set_facecolor(P_BG_CREAM)
                        cell.set_text_props(color=P_TEXT_BROWN, size=11)
            else:
                ax.text(0.5, 0.5, "No Success Data", ha='center', va='center', color=P_TEXT_BROWN, fontweight='bold')
        else:
            ax.text(0.5, 0.5, "No Success Data", ha='center', va='center', color=P_TEXT_BROWN, fontweight='bold')


        ax = axes[0, 1]
        style_cute_ax(ax, "Avg Time to Complete Level")
        if not level_results.empty:
            success_df = level_results[level_results["Value2"] == "SUCCESS"].copy()
            if not success_df.empty:
                success_df["Level"] = pd.to_numeric(success_df["Level"])
                avg_time_per_level = success_df.groupby("Level")["Value1"].mean()
                ax.plot(avg_time_per_level.index, avg_time_per_level.values, marker='o', color=P_SIENNA, markerfacecolor=P_TERRACOTTA, markeredgecolor=P_TEXT_BROWN, markersize=10)
                ax.set_xlabel("Level", color=P_TEXT_BROWN, fontweight='bold')
                ax.set_ylabel("Seconds", color=P_TEXT_BROWN, fontweight='bold')
                ax.set_xticks(avg_time_per_level.index) 
            else:
                ax.text(0.5, 0.5, "No Success Data", ha='center', va='center', color=P_TEXT_BROWN, fontweight='bold')
        else:
            ax.text(0.5, 0.5, "No Data", ha='center', va='center', color=P_TEXT_BROWN, fontweight='bold')


        ax = axes[0, 2]
        style_cute_ax(ax, "Ingredient Waste Ratio")
        waste = df[df["EventType"] == "Waste_Event"].copy()
        
        valid_ingredients = ['cabbage', 'beef', 'fish', 'rice']
        waste = waste[waste["Item"].str.lower().isin(valid_ingredients)]
        
        if not waste.empty:
            waste_counts = waste["Item"].value_counts()
            
            color_map = {
                'cabbage': P_ARTICHOKE, 
                'beef': P_SIENNA,       
                'fish': P_TAN,          
                'rice': P_TERRACOTTA    
            }
            colors = [color_map.get(str(item).lower(), P_TAN) for item in waste_counts.index]
            labels = [str(item).capitalize() for item in waste_counts.index]
            
            patches, texts, autotexts = ax.pie(waste_counts, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
            
            for patch in patches:
                patch.set_joinstyle('round')
                
            for t in texts: t.set_color(P_TEXT_BROWN); t.set_fontweight('bold')
            for at in autotexts: at.set_color(P_BG_CREAM); at.set_fontweight('bold')
        else:
            ax.text(0.5, 0.5, "No Waste Recorded", ha='center', va='center', color=P_TEXT_BROWN, fontweight='bold')
            

        ax = axes[1, 0]
        style_cute_ax(ax, "Click Distribution (2D Bin)")
        clicks = df[df["EventType"] == "Click_Position"].copy()
        if not clicks.empty:
            clicks["Value1"] = pd.to_numeric(clicks["Value1"])
            clicks["Value2"] = pd.to_numeric(clicks["Value2"])
            mask = (clicks["Value1"] < 1024) & (clicks["Value2"] < 720)
            
            h = ax.hist2d(clicks[mask]["Value1"], clicks[mask]["Value2"], 
                          bins=[20, 15], range=[[0, 1024], [0, 720]], 
                          cmap='Oranges')
            
            ax.set_xlim(0, 1024)
            ax.set_ylim(720, 0)
            ax.set_xlabel("X Coordinate", color=P_TEXT_BROWN, fontweight='bold')
            ax.set_ylabel("Y Coordinate", color=P_TEXT_BROWN, fontweight='bold')
        else:
            ax.text(0.5, 0.5, "No Clicks Recorded", ha='center', va='center', color=P_TEXT_BROWN, fontweight='bold')


        ax = axes[1, 1]
        style_cute_ax(ax, "Crop Harvest Yields")
        harvests = df[df["EventType"] == "Harvest"].copy()
        if not harvests.empty:
            harvest_counts = harvests["Item"].value_counts()
            bars = ax.bar(harvest_counts.index, harvest_counts.values)
            
            color_map = {
                'cabbage': P_ARTICHOKE, 
                'beef': P_SIENNA,       
                'fish': P_TAN,          
                'rice': P_TERRACOTTA    
            }
            
            for i, bar in enumerate(bars):
                item_name = str(harvest_counts.index[i]).lower()
                bar.set_facecolor(color_map.get(item_name, P_TAN))
                bar.set_joinstyle('round') 
                
            ax.set_xlabel("Crop Type", color=P_TEXT_BROWN, fontweight='bold')
            ax.set_ylabel("Quantity", color=P_TEXT_BROWN, fontweight='bold')
            ax.tick_params(axis='x', rotation=0)
            for label in ax.get_xticklabels():
                label.set_fontweight('bold')
        else:
            ax.text(0.5, 0.5, "No Crops Harvested", ha='center', va='center', color=P_TEXT_BROWN, fontweight='bold')
            

        ax = axes[1, 2]
        style_cute_ax(ax, "Interaction Frequency Spread")
        interactions = df[df["EventType"] == "Interaction"].copy()
        if not interactions.empty:
            pivot = interactions.groupby(['Level', 'Item']).size().unstack(fill_value=0)
            if not pivot.empty:
                box_data = [pivot[col] for col in pivot.columns]
                
                pretty_labels = [str(item).replace('Field_', '').replace('_', ' ').title() for item in pivot.columns]
                
                bp = ax.boxplot(box_data, patch_artist=True, labels=pretty_labels, notch=False, vert=True)

                for box in bp['boxes']:
                    box.set(facecolor=P_SIENNA, edgecolor=P_TEXT_BROWN) 
                    box.set_joinstyle('round')
                for whisker in bp['whiskers']:
                    whisker.set(color=P_TEXT_BROWN)
                for cap in bp['caps']:
                    cap.set(color=P_TEXT_BROWN)
                for median in bp['medians']:
                    median.set(color=P_TERRACOTTA, linewidth=4, solid_capstyle='round') 
                for flier in bp['fliers']:
                    flier.set(marker='o', markerfacecolor=P_ARTICHOKE, markeredgecolor=P_TEXT_BROWN, alpha=0.7, markersize=6) 

                ax.set_xlabel("Interaction Target", color=P_TEXT_BROWN, fontweight='bold')
                ax.set_ylabel("Interaction Count", color=P_TEXT_BROWN, fontweight='bold')
                
                ax.tick_params(axis='x', rotation=45)
                for tick in ax.get_xticklabels():
                    tick.set_horizontalalignment('right')
                    tick.set_fontweight('bold')
            else:
                ax.text(0.5, 0.5, "No Data", ha='center', va='center', color=P_TEXT_BROWN, fontweight='bold')
        else:
            ax.text(0.5, 0.5, "No Interactions", ha='center', va='center', color=P_TEXT_BROWN, fontweight='bold')

        plt.tight_layout(pad=3.0)
        fig.subplots_adjust(top=0.90)

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        def clean_quit():
            plt.close('all')
            root.quit()
            root.destroy()
            os._exit(0)

        root.protocol("WM_DELETE_WINDOW", clean_quit)

        btn = tk.Button(root, text="Close & Exit", command=clean_quit, font=("Comic Sans MS", 14, "bold"), bg=P_TAN, fg=P_TEXT_BROWN, relief="ridge", borderwidth=4)
        btn.pack(pady=10)

        root.mainloop()

if __name__ == "__main__":
    game = Game()
    game.run()