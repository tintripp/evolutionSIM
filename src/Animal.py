import pygame
import util
import random
from constants import *
import time
class Animal:
    img = pygame.image.load(util.path("resources", "banjo.png")).convert_alpha() 
    animations = util.read_json(util.path("resources", "banjo.json"))

    def __init__(self,x,y,parents=[]):
        self.x=x
        self.y=y
        self.parents = parents

        self.color = random.randint(0,360)
        self.img = util.hue_shift_img(Animal.img, self.color)

        self.anim_frame = 0
        self.anim_name = "down"
    
    def update(self, dt):
        self.anim_frame = int(time.time()) % len(Animal.animations[self.anim_name])#len of curanim
    
    def draw(self, screen, cam):
        anim = Animal.animations[self.anim_name][self.anim_frame]
        offset = [
            Animal.animations["xOff"] if "xOff" in Animal.animations else 0,
            Animal.animations["yOff"] if "yOff" in Animal.animations else 0
        ]

        scaled = pygame.transform.scale_by(self.img.subsurface(
            pygame.Rect(anim["x"],anim["y"],anim["w"],anim["h"])
        ),cam.zoom/MAP_MAX_SCALE)

        screen.blit(scaled, 
            dest=scaled.get_frect(
                centerx=(self.x/MAP_MAX_SCALE*cam.zoom)+cam.x+offset[0],
                bottom=(self.y/MAP_MAX_SCALE*cam.zoom)+cam.y+offset[1]
            )
        )


def create_animals(world,min,max):
    #create the first animals
    animals=[]

    spawn_areas = util.indices_higher_than(world.heights, world.waterlevel + (TERRAIN_GRASS_HEIGHT*2))

    for _ in range(random.randint(min,max)):
        spawn_area = spawn_areas[random.randint(min,len(spawn_areas)-1)]
        animals.append(
            Animal(
                spawn_area[0]*MAP_MAX_SCALE, spawn_area[1]*MAP_MAX_SCALE
            )
        )
    return animals