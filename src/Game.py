import pygame
import random
from constants import *
from World import World

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
        self.world = World(123)

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
            self.world.update(event)
    def update(self, dt):
        self.world.update(dt)
    def draw(self):
        self.screen.fill(0)

        self.world.draw(self.screen)

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