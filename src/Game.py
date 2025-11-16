import pygame
from constants import *
from World import World

class Game:
    def __init__(self):

        self.done = False
        self.clock = pygame.time.Clock()

        self.window = pygame.display.set_mode(
            (MAP_WIDTH*WINDOW_INIT_SCALE, MAP_HEIGHT*WINDOW_INIT_SCALE), pygame.RESIZABLE
        )
        self.screen = pygame.Surface((MAP_WIDTH, MAP_HEIGHT))
        pygame.init()
        pygame.display.init()

        #generate world
        self.world = World(MAP_WIDTH, MAP_HEIGHT)

        #this looks weird here, but i MUST import AFTER calling set_mode
        from Animal import create_animals

        self.animals = create_animals(self.world, 1, 1)


    def handle_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.done =True
            self.world.handle_event(event)
    def update(self, dt):
        self.world.update(dt)
        for animal in self.animals:
            animal.update(dt, self.world)
        
    def draw(self):
        self.screen.fill(0)

        self.world.draw(self.screen)

        for animal in self.animals:
            animal.draw(self.screen, self.world.cam)

        font = pygame.font.SysFont("notomono", 24)
        fps_text = font.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255)) # White text
        self.screen.blit(fps_text, (10, 10)) # Display at top-left corner

        self.window.blit(
            pygame.transform.scale(self.screen,pygame.display.get_surface().get_size())
        )
    def loop(self):
        while not self.done:
            dt = self.clock.tick(FPS)

            self.handle_events()
            self.update(dt)
            self.draw()

            pygame.display.flip()