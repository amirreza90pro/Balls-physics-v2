import cv2
import numpy as np
import time
import math
import classes
import pandas as pd
import keyboard
import random
import cv2
import io
import comtypes.client
import ctypes
from PIL import Image
import os
import tempfile
import copy


w, h = 1366, 698
rw, rh = w, h
n = w / h
radius = 0.075
balans = 0.20
Approximation_factor = 2 # pixels


particels_dict = {
    'number' : 50,
    'class_num' : 3,
    'colors' : [(0, 0, 255), (255, 0 , 0), (0, 255 , 0)]
}


physics = classes.physics()
Screen = classes.Screen('Particel Life', (rw, rh), physics.m_to_pix)
Particels = classes.Particels(particels_dict, (rw, rh), balans, physics.m_to_pix)


# should not change :
last_time = time.time()
this_time = time.time()


    
while True:
    Screen.clear()
    # Screen.screen = Screen.screen - Screen.screen//3
    
    last_time = copy.deepcopy(this_time)
    this_time = time.time()
    delay = this_time - last_time
    touch_ground = False
    
    lk = keyboard.is_pressed('left')
    rk = keyboard.is_pressed('right')
    uk = keyboard.is_pressed('up')
    dk = keyboard.is_pressed('down')


    # if particle[3][0] > 12: particle[3][0] = 12
    # elif particle[3][0] < -12: particle[3][0] = -12
    # if particle[3][1] > 12: particle[3][1] = 12
    # elif particle[3][1] < -12: particle[3][1] = -12
    

    for particle_index in range(Particels.number):
        particle = [
            Particels.classes[particle_index], 
            Particels.colors[Particels.classes[particle_index]], 
           [Particels.x[particle_index], Particels.y[particle_index]],
           [Particels.speedX[particle_index], Particels.speedY[particle_index]],
            Particels.mass[particle_index]
        ]
        
        Fx = 0
        Fy = 0
        radius = particle[4]
        
        if lk: Fx -= 1.7
        elif rk: Fx += 1.7
        if uk: Fy -= 1.7
        elif dk: Fy += 1.7

        # apply gravity
        Fy += physics.gravity * particle[4]    # w = m.g
        
        
        # air ressistance
        Fx += physics.air_ressistance(radius, particle[3][0])
        Fy += physics.air_ressistance(radius, particle[3][1])
            
            
        # Particels.touching(particle, particle_index, radius * physics.m_to_pix)
        Particels.outed(particle, radius)
        
        
        # touching
        if Particels.screenym-radius <= particle[2][1] <= Particels.screenym-radius:
          Fy -= physics.gravity * particle[4]
          touch_ground = True
        
        
        # friction
        if abs(Fx)<(physics.gravity * particle[4] * Particels.friction_s) and particle[3][0] == 0: Fx = 0
        elif touch_ground: Fx += -1 * (physics.gravity * particle[4] * Particels.friction_k * Fx) / abs(Fx)
        
        
        # apply speed
        particle[3][0] += (Fx / particle[4]) * delay  # v = f/m.t
        particle[3][1] += (Fy / particle[4]) * delay
        particle[2][0] += particle[3][0] * delay    # x = v.t
        particle[2][1] += particle[3][1] * delay     
        
        
        # ending proccesses
        Particels.classes[particle_index] = particle[0]
        Particels.x[particle_index] = particle[2][0]
        Particels.y[particle_index] = particle[2][1]
        Particels.speedX[particle_index] = particle[3][0]
        Particels.speedY[particle_index] = particle[3][1]

        Screen.render_particle(particle, int(radius * physics.m_to_pix))
        

    # Screen.blur((5, 5))
    cv2.imshow(Screen.title, cv2.resize(Screen.screen, (w, h)))

    if cv2.waitKey(2) & 0xFF == ord('q'):
        break

    

cv2.destroyAllWindows()