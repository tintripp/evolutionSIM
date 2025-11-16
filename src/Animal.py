import pygame
import numpy
import util
import random
from constants import *
from World import World

class Animal:
    img = pygame.image.load(util.path("resources", "banjo.png")).convert_alpha() 
    animations = util.read_json(util.path("resources", "banjo.json"))

    def __init__(self,world,x,y,parents=[]):
        #this should be in TILES, and 
        # there should be another set of X and Y that are FLOATS and FOR DRAWING that look nice.
        self.world = world

        self.targetx=x
        self.targety=y
        self.x=self.targetx
        self.y=self.targety
        self.velx=0
        self.vely=0

        self.sightradius=10
        
        self.pick_new_target(world)


        self.parents = parents

        self.color = random.randint(0,360)
        self.img = util.hue_shift_img(Animal.img, self.color)
        self.rect=None

        self.anim_frame = -1
        self.anim_name = "down"

    def _update_anims(self):
        #get right anim
        if(self.vely):
            self.anim_name = "down" if(self.vely > 0) else "up"
        elif(self.velx):
            self.anim_name = "right" if(self.velx > 0) else "left"

        
        #increase frame
        magnitude = util.get_magnitude((self.velx,self.vely))
        if(magnitude > 0.4):
            self.anim_frame += magnitude / 1000
        else:
            self.anim_frame =-1 # last

    def pick_new_target(self, world: World):
        targets =world.get_land_within_radius(self.targetx,self.targety ,self.sightradius)
        if(targets.shape[0]==0): 
            print('dude i cant move! len of targets:', len(targets))
            return #could not find a tile to move to, so don't.
        
        self.targetx,self.targety= targets[numpy.random.randint(0, targets.shape[0])]

    def update(self, dt, world):
        
        speed = 0.04  # tiles per second

        self.velx = self.targetx - self.x
        self.vely = self.targety - self.y

        # Move toward target tile
        dt =min(dt, 0.05)  
        self.x += self.velx * dt * speed
        self.y += self.vely * dt * speed

        # Reached tile?
        if abs(self.velx) < 0.05 and abs(self.vely) < 0.05:
            self.x = self.targetx
            self.y = self.targety
            self.pick_new_target(world)
        

        self._update_anims()

    def draw(self, screen, cam):
        anim_frames= Animal.animations[self.anim_name]
        anim = anim_frames[int(self.anim_frame)%len(anim_frames)]
        offset = [
            anim["xOff"] if "xOff" in anim else 0,
            anim["yOff"] if "yOff" in anim else 0
        ]

        scaled = pygame.transform.scale_by(self.img.subsurface(
            pygame.Rect(anim["x"],anim["y"],anim["w"],anim["h"])
        ),cam.zoom/MAP_MAX_SCALE)
        self.rect=scaled.get_frect(
            centerx=((self.x+(offset[0]//cam.zoom))*cam.zoom)+cam.x,
            bottom=((self.y+(offset[1]//cam.zoom))*cam.zoom)+cam.y
        )

        screen.blit(scaled, 
            dest=self.rect
        )


def create_animals(world,min,max):
    #create the first animals
    animals=[]

    spawn_areas = util.indices_higher_than(world.heights, world.waterlevel + (TERRAIN_GRASS_HEIGHT*2))

    for _ in range(random.randint(min,max)):
        spawn_area = spawn_areas[random.randint(min,len(spawn_areas)-1)]
        animals.append(
            Animal(
                world, 
                spawn_area[0], spawn_area[1]
            )
        )
    return animals