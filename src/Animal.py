import pygame
import os
import util
import random
class Animal:
    img = pygame.image.load(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/resources/banjo.png"
    ).convert_alpha() 

    def __init__(self,x,y,parents=[]):
        self.x=x
        self.y=y
        self.parents = parents

        self.color = random.randint(0,360)
        self.img = util.hue_shift_img(Animal.img, self.color)
    
    def draw(self, screen):
        screen.blit(self.img, (self.x,self.y))

