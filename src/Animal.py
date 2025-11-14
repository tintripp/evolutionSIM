import pygame
import json
import util
import random
from constants import *
class Animal:
    img = pygame.image.load(util.get_path("resources", "banjo.png")).convert_alpha() 
    dat = json.load

    def __init__(self,x,y,parents=[]):
        self.x=x
        self.y=y
        self.parents = parents

        self.color = random.randint(0,360)
        self.img = util.hue_shift_img(Animal.img, self.color)
    
    def draw(self, screen, cam):
        scaled = pygame.transform.scale_by(self.img,cam.zoom/MAP_MAX_SCALE)

        screen.blit(scaled, scaled.get_frect(
            centerx=(self.x/MAP_MAX_SCALE*cam.zoom)+cam.x,
            bottom=(self.y/MAP_MAX_SCALE*cam.zoom)+cam.y
        ))


def create_animals(world,min,max):
    #create the first animals
    animals=[]

    spawn_areas = util.indices_higher_than(world.heights, world.waterlevel + (TERRAIN_GRASS_HEIGHT*2))


    for i in range(random.randint(min,max)):
        spawn_area = spawn_areas[random.randint(min,len(spawn_areas)-1)]
        animals.append(
            Animal(
                spawn_area[0]*MAP_MAX_SCALE, spawn_area[1]*MAP_MAX_SCALE
            )
        )
    return animals