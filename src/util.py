import pygame
from constants import *
import noise
def hue_shift_img(image,deg):
    # Create a copy of the image to modify
    modified_image = image.copy()

    # Lock the surface for pixel manipulation
    pixel_array = pygame.PixelArray(modified_image)

    # Define the hue shift amount (in degrees, 0-360)
    hue_shift_amount = deg  # Example: shift hue by 90 degrees

    for x in range(modified_image.get_width()):
        for y in range(modified_image.get_height()):
            # Get the color of the current pixel
            pixel_color = modified_image.unmap_rgb(pixel_array[x, y])

            # Convert to HSL
            h, s, l, a = pixel_color.hsla

            # Shift the hue
            h = (h + hue_shift_amount) % 360

            # Set the new HSL values
            pixel_color.hsla = (h, s, l, a)

            # Update the pixel in the PixelArray
            pixel_array[x, y] = pixel_color

    # Unlock the surface
    del pixel_array

    return modified_image

def make_noise_map(width,height,seed):
    noisemap=[]
    for x in range(width):
        row = []

        for y in range(height):
            z = noise.pnoise2(
                x * NOISE_SCALE, 
                y * NOISE_SCALE, 
                octaves= NOISE_OCTAVES, 
                persistence= NOISE_PERSISTENCE, 
                lacunarity= NOISE_LACUNARITY, 
                repeatx= WINDOW_WIDTH, 
                repeaty= WINDOW_HEIGHT, 
                base=2
            )
            print(z)
            
            z = int((z+1)*255)
            
            row.append(z)

        noisemap.append(row)
    return noisemap