import pygame
from constants import *

def clamp(value,minmax):
    return min(max(value,minmax[0]),minmax[1])

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

def indices_higher_than(arr,thres):
    indices=[]

    for i in range(arr.shape[0]): 
        for j in range(arr.shape[1]): 
            if arr[i, j]>thres:
                indices.append((i,j))

    return indices