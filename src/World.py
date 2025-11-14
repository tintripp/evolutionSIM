import pygame
from constants import *
import util
import noise
import numpy

class World:
    def __init__(self, width, height ,seed):
        self.width=width
        self.height=height
        self.seed=seed

        #numpy array
        self.heights = self._make_heightmap(width, height, seed)

        #the surface that we draw! YAY!!!
        self.surface = pygame.Surface((width, height))

        # Later, update it quickly from a NumPy array
        #pygame.surfarray.blit_array(self.surface, rgb_array)


        #COOL
        self.waterlevel=110

        #camera
        self.camzoom=1
        self.camx=0
        self.camy=0
        self.scrollvel=0
        

    def _make_heightmap(self,width,height,seed):
        noisemap= numpy.empty((width,height))

        seed = hash(seed) & 0x7FFF
        print(seed)

        for x in range(width):
            for y in range(height):
                z = noise.snoise2(
                    x * NOISE_SCALE, 
                    y * NOISE_SCALE, 
                    octaves= NOISE_OCTAVES, 
                    persistence= NOISE_PERSISTENCE, 
                    lacunarity= NOISE_LACUNARITY, 
                    base= seed
                )
                
                noisemap[x][y]=z

        noisemap = numpy.clip(noisemap, -1.0, 1.0)
        noisemap = ((noisemap + 1.0) * (255 / 2)).astype(numpy.uint8)

        return noisemap
    
    def _get_colormap(self):
        rgb = numpy.empty((self.width, self.height, 3), dtype=numpy.uint8)

        # Base water color
        rgb[..., 0] = 30 + (self.heights - 30)
        rgb[..., 1] = 30 + (self.heights - 30)
        rgb[..., 2] = 200

        # Sand
        mask_sand = self.heights > self.waterlevel
        rgb[mask_sand] = (255, 234, 163)

        # Land
        mask_land = self.heights > (self.waterlevel + 7)
        rgb[mask_land, 0] = 0
        rgb[mask_land, 1] = 120 + (self.heights[mask_land] - 120)
        rgb[mask_land, 2] = 0

        return rgb
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            self.scrollvel+=event.y/50

    def update(self, dt):
        #testing
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_w]): self.waterlevel+=1
        if (keys[pygame.K_s]): self.waterlevel-=1

        # camera 
        mouse_x, mouse_y = pygame.mouse.get_pos()
        win_w,win_h = pygame.display.get_surface().get_size()

        mouse_x/=win_w/WINDOW_WIDTH
        mouse_y/=win_h/WINDOW_HEIGHT

        #get where mouse is on our og surface
        cursor_rel_x = (mouse_x - self.camx) / self.camzoom
        cursor_rel_y = (mouse_y - self.camy) / self.camzoom

        #apply zoom
        self.camzoom+=self.scrollvel
        self.camzoom=util.clamp(self.camzoom,(1,5))
        self.scrollvel*=0.8

        #move to keep world under mouse centered
        self.camx = mouse_x - cursor_rel_x * self.camzoom
        self.camy = mouse_y - cursor_rel_y * self.camzoom

        #clamp
        if(-self.camx<0): self.camx=0
        if(-self.camy<0): self.camy=0
        if((self.camx+WINDOW_WIDTH)*self.camzoom<WINDOW_WIDTH): #fix
            print('rightmost')

    def draw(self, screen):
        pygame.surfarray.blit_array(self.surface, self._get_colormap())
    
        screen.blit(
            pygame.transform.scale_by(self.surface,self.camzoom), 
            (self.camx,self.camy)
        )