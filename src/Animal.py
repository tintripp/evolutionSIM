import pygame
import util
import random
from constants import *
from World import World
import time
class Animal:
    img = pygame.image.load(util.path("resources", "banjo.png")).convert_alpha() 
    animations = util.read_json(util.path("resources", "banjo.json"))

    def __init__(self,x,y,parents=[]):
        #this should be in TILES, and 
        # there should be another set of X and Y that are FLOATS and FOR DRAWING that look nice.
        self.x=x
        self.y=y


        self.parents = parents

        self.color = random.randint(0,360)
        self.img = util.hue_shift_img(Animal.img, self.color)

        self.anim_frame = -1
        self.anim_name = "down"
    
    def update(self, dt, world: World):
        self.anim_frame = int(time.time()) % len(Animal.animations[self.anim_name])#len of curanim

        #get right anim
        """
        if(vector.y):
            this.animName = (vector.y > 0) ? "down" : "up"
        elif(vector.x):
            this.animName = (vector.x > 0) ? "right" : "left"

        //increase frame
        const magnitude = getMagnitude(this.velocity);
        if(magnitude > 0.4){
            this.animFrame += magnitude / 16;
        }else{
            this.animFrame = this.animations[this.animName].length - 1; // last
        }"""

    """
    def update(animal, dt):
        # animal.tx, animal.ty = tile target
        # animal.x,  animal.y  = current float position

        speed = 5.0  # tiles per second

        dx = animal.tx - animal.x
        dy = animal.ty - animal.y

        # Move toward target tile
        animal.x += dx * dt * speed
        animal.y += dy * dt * speed

        # Reached tile?
        if abs(dx) < 0.05 and abs(dy) < 0.05:
            animal.x = animal.tx
            animal.y = animal.ty
            pick_new_target(animal, world)
    """

    def draw(self, screen, cam):
        anim = Animal.animations[self.anim_name][self.anim_frame]
        offset = [
            anim["xOff"] if "xOff" in anim else 0,
            anim["yOff"] if "yOff" in anim else 0
        ]

        scaled = pygame.transform.scale_by(self.img.subsurface(
            pygame.Rect(anim["x"],anim["y"],anim["w"],anim["h"])
        ),cam.zoom/MAP_MAX_SCALE)

        screen.blit(scaled, 
            dest=scaled.get_frect(
                centerx=((self.x+offset[0])/MAP_MAX_SCALE*cam.zoom)+cam.x,
                bottom=((self.y+offset[1])/MAP_MAX_SCALE*cam.zoom)+cam.y
            )
        )


def create_animals(world,min,max):
    #create the first animals
    animals=[]

    spawn_areas = util.indices_higher_than(world.heights, world.waterlevel + (TERRAIN_GRASS_HEIGHT*2))

    for _ in range(random.randint(min,max)):
        spawn_area = spawn_areas[random.randint(min,len(spawn_areas)-1)]
        animals.append(
            Animal(
                spawn_area[0]*MAP_MAX_SCALE, spawn_area[1]*MAP_MAX_SCALE
            )
        )
    return animals