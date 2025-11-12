import pygame
import random
from constants import *
import util
import time

class Game:
    def __init__(self):

        self.done = False
        self.clock = pygame.time.Clock()

        self.window = pygame.display.set_mode(
            (WINDOW_WIDTH*WINDOW_INIT_SCALE, WINDOW_HEIGHT*WINDOW_INIT_SCALE), pygame.RESIZABLE
        )
        self.screen = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.init()
        pygame.display.init()

        #generate world
        self.world = util.make_noise_map(WINDOW_WIDTH, WINDOW_HEIGHT, int(time.time()*1000))

        #this looks weird here, but i MUST import AFTER calling set_mode
        from Animal import Animal
        self.animals = []

        #create the first animals
        for i in range(random.randint(2,9)):
            self.animals.append(
                Animal(
                    random.randint(0, WINDOW_WIDTH-Animal.img.get_width()),
                    random.randint(0, WINDOW_HEIGHT-Animal.img.get_height())
                )
            )
    def handle_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.done =True
    def update(self, dt):
        pass
    def draw(self):
        for x in range(len(self.world)):
            for y in range(len(self.world[x])):
                z = self.world[x][y]

                """color = (30+z,0+z,255)
                if z>110:
                    color = (111,111,0)"""
                self.screen.set_at((x,y), (z,)*3)#color)
            

        for a in self.animals:
            a.draw(self.screen)

        self.window.blit(
            pygame.transform.scale(self.screen,pygame.display.get_surface().get_size())
        )
    def loop(self):
        while not self.done:
            dt = self.clock.tick(60)

            self.handle_events()
            self.update(dt)
            self.draw()

            pygame.display.flip()