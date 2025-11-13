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

        #COOL
        self.waterlevel=110
        self.camzoom=1
        self.camx=0
        self.camy=0

        #generate world
        self.world = util.make_noise_map(WINDOW_WIDTH, WINDOW_HEIGHT, 123)

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
            elif event.type == pygame.MOUSEWHEEL:
                self.camzoom+=event.y/100
                self.camx=-self.camzoom*100
    def update(self, dt):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_w]): self.waterlevel+=1
        if (keys[pygame.K_s]): self.waterlevel-=1
    def draw(self):
        self.screen.fill(0)
        print(self.camx,self.camy)
        for x in range(len(self.world)):
            for y in range(len(self.world[x])):
                z = self.world[x][y]

                color = (30+(z-30),30+(z-30),200)#water
                if z>self.waterlevel:
                    color = (0,120+(z-120),0)#land

                color=tuple(c%255 for c in color)

                
                #self.screen.set_at((y,x), color)
                pygame.draw.rect(self.screen,color,pygame.Rect(
                    (y*self.camzoom)+self.camx,(x*self.camzoom)+self.camy,self.camzoom,self.camzoom
                ))

            

        for a in self.animals:
            a.draw(self.screen)

        font = pygame.font.SysFont("notomono", 24)
        fps_text = font.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255)) # White text
        self.screen.blit(fps_text, (10, 10)) # Display at top-left corner

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