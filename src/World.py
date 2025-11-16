import pygame
from constants import *
import util
import noise
import time
import numpy

class WorldCamera:
    def __init__(self, x=0, y=0, zoom=1):
        self.zoom=zoom
        self.x=x
        self.y=y
        self.scrollvel=0

    def _clamp_position(self, min_x, min_y, max_x, max_y):
        if(-self.x < min_x): 
            self.x = min_x
        if(-self.y < min_y): 
            self.y = min_y
        if(((-self.x+max_x)/self.zoom)>max_x):
            self.x=max_x-(max_x*self.zoom)
        if(((-self.y+max_y)/self.zoom)>max_y):
            self.y=max_y-(max_y*self.zoom)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            self.scrollvel+=event.y*(CAM_SCROLL_SPEED_MULT/100)

    def update(self, dt):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        win_w,win_h = pygame.display.get_surface().get_size()
        win_relw,win_relh=(win_w/MAP_WIDTH,win_h/MAP_HEIGHT)

        mouse_x/=win_relw
        mouse_y/=win_relh

        #get where mouse is on our og surface
        cursor_rel_x = (mouse_x - self.x) / self.zoom
        cursor_rel_y = (mouse_y - self.y) / self.zoom

        #apply zoom
        self.zoom+=self.scrollvel
        self.zoom=util.clamp(self.zoom,(MAP_MIN_SCALE,MAP_MAX_SCALE))
        self.scrollvel*=0.95

        #print(round(self.zoom,2))

        #move to keep world under mouse centered
        self.x = mouse_x - cursor_rel_x * self.zoom
        self.y = mouse_y - cursor_rel_y * self.zoom

        #pan camera with middle mouse button
        relx,rely=pygame.mouse.get_rel()
        if (pygame.mouse.get_pressed()[2]):
            self.x+=relx/win_relw
            self.y+=rely/win_relh

        self._clamp_position(0, 0, MAP_WIDTH, MAP_HEIGHT)

class World:
    def __init__(self, width, height ,seed=None):
        self.width=width
        self.height=height
        if(not seed):seed=time.time()
        self.seed=seed

        #numpy array
        self.heights = self._make_heightmap(width, height, seed)

        #COOL
        self.waterlevel=160

        #the surface that we draw! YAY!!!
        self.surface = pygame.Surface((width, height))
        self.needs_refresh=True

        #camera
        self.cam=  WorldCamera(zoom=MAP_MIN_SCALE)

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

        #water
        rgb[..., 0] = 30 + (self.heights - 30)
        rgb[..., 1] = 30 + (self.heights - 30)
        rgb[..., 2] = 200

        #sand
        mask_sand = self.heights > self.waterlevel
        rgb[mask_sand] = (255, 234, 163)

        #land
        mask_land = self.heights > (self.waterlevel + TERRAIN_GRASS_HEIGHT)
        rgb[mask_land, 0] = 0
        rgb[mask_land, 1] = 120 + (self.heights[mask_land] - 120)
        rgb[mask_land, 2] = 0

        return rgb
    
    def set_waterlevel(self, amt):
        self.waterlevel=amt
        self.needs_refresh=True
    def change_waterlevel_by(self, amt):
        self.set_waterlevel(self.waterlevel+amt)

    def get_land_within_radius(self, px, py, radius):
        h, w = self.heights.shape #height, width
        Y, X = numpy.ogrid[:h, :w]

        mask = (
            (X - px)**2 + (Y - py)**2 <= radius * radius
        ) & (self.heights > self.waterlevel)

        coords = numpy.argwhere(mask) #return all elements where mask is true!
        return coords

    
    def handle_event(self, event):
        self.cam.handle_event(event)

    def update(self, dt):
        #testing
        """
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_w]): self.change_waterlevel_by(1)
        if (keys[pygame.K_s]): self.change_waterlevel_by(-1)"""

        self.cam.update(dt)

    def draw(self, screen):
        if self.needs_refresh:
            pygame.surfarray.blit_array(self.surface, self._get_colormap())
            self.needs_refresh = False

        screen_w, screen_h = screen.get_size()

        world_x = -self.cam.x / self.cam.zoom
        world_y = -self.cam.y / self.cam.zoom
        int_x = int(world_x)
        int_y = int(world_y)

        view_rect = pygame.Rect(
            int_x,
            int_y,
            int(screen_w / self.cam.zoom) + 2,
            int(screen_h / self.cam.zoom) + 2
        )
        
        clip_rect = view_rect.clip(pygame.Rect(0, 0, self.width, self.height))
        sub = self.surface.subsurface(clip_rect)

        scaled = pygame.transform.scale(
            sub, (
                int(clip_rect.width * self.cam.zoom),
                int(clip_rect.height * self.cam.zoom)
            )
        )
        
        screen.blit(scaled, (
            -(world_x - int_x) * self.cam.zoom,
            -(world_y - int_y) * self.cam.zoom
        ))