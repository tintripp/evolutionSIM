import pygame
from constants import *
import util

class World:
    def __init__(self, seed):
        self.seed=seed

        self.heights = util.make_noise_map(WINDOW_WIDTH, WINDOW_HEIGHT, self.seed)

        #COOL
        self.waterlevel=110
        self.camzoom=1
        self.camx=0
        self.camy=0
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            self.camzoom+=event.y/100
            self.camx=-self.camzoom*100
    def update(self, dt):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_w]): self.waterlevel+=1
        if (keys[pygame.K_s]): self.waterlevel-=1
    def draw(self, screen):

        for x in range(len(self.heights)):
            for y in range(len(self.heights[x])):
                z = self.heights[x][y]

                color = (30+(z-30),30+(z-30),200)#water
                if z>self.waterlevel:
                    color = (255, 234, 163)#sand
                if z>self.waterlevel+7:
                    color = (0,120+(z-120),0)#land

                color=tuple(c%256 for c in color)

                
                #screen.set_at((y,x), color)
                pygame.draw.rect(screen,color,pygame.Rect(
                    (y*self.camzoom)+self.camx,(x*self.camzoom)+self.camy,self.camzoom,self.camzoom
                ))