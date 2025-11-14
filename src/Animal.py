import pygame
import os
import util
import random
from constants import *
class Animal:
    img = pygame.image.load(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/resources/banjohd.png"
    ).convert_alpha() 

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


def create_animals(min,max):
    #create the first animals
    animals=[]
    for i in range(random.randint(min,max)):
        animals.append(
            Animal(
                random.randint(0, (MAP_WIDTH*MAP_MAX_SCALE)),
                random.randint(0, (MAP_HEIGHT*MAP_MAX_SCALE))
            )
        )
    return animals