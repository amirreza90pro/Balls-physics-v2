import numpy as np
import math, cv2
import random, time
import pandas as pd
from matplotlib import pyplot

touchHitBox = 0.5

def np_to_better_np(arr):
    p = pd.DataFrame(arr)
    a = np.array(p)
    return a


def distance(x, y):
    return math.sqrt((x ** 2) + (y ** 2))


class Screen:
    def __init__(self, title, xy, m_to_pix):
        self.m_to_pix = m_to_pix
        self.title = title
        self.x, self.y = xy[0], xy[1]
        self.screen = np.zeros((self.y, self.x, 3))


    def clear(self):
        self.screen = np.zeros((self.y, self.x, 3))
    
    def render_particle(self, particle, r):
        self.screen = cv2.circle(self.screen, (int(particle[2][0] * self.m_to_pix), int(particle[2][1] * self.m_to_pix)), int(r), particle[1], -1)


    def blur(self, blur):
        self.screen = cv2.blur(self.screen, blur)



class Particels:
    def __init__(self, particels_dict, wh, balance, m_to_pix):
        self.screenx, self.screeny = wh
        self.screenxm, self.screenym = wh[0]/m_to_pix, wh[1]/m_to_pix
        self.particels_dict = particels_dict
        self.balance = balance
        self.m_to_pix = m_to_pix
        self.friction_s = 1.5
        self.friction_k = 1
        

        self.number = particels_dict['number']
        self.class_num = particels_dict['class_num']
        self.colors = particels_dict['colors']

        self.x = np.random.randint(0, self.screenx, size=self.number)
        self.y = np.random.randint(0, self.screeny, size=self.number)
        self.x = self.x.astype(np.float64) / m_to_pix
        self.y = self.y.astype(np.float64) / m_to_pix

        self.classes = np.random.randint(self.class_num, size=self.number)
        self.speedX = np.zeros(self.number)
        self.speedY = np.zeros(self.number)
        
        # self.mass = np.where(np.zeros(self.number) == 0, 0.115, 0.115)
        self.mass = np.random.randint(90, 125, size=self.number) / 1000



    def outed(self, particle, radius):
        if particle[2][1] > self.screenym-radius:
            particle[2][1] = self.screenym-radius ; particle[3][1] = round(particle[3][1]*self.balance*-1)
            
        elif particle[2][1] < radius:
            particle[2][1] = radius ; particle[3][1] = round(abs(particle[3][1]*self.balance))
            
        if particle[2][0] > self.screenxm-radius:
            particle[2][0] = self.screenxm - radius ; particle[3][0] = round(particle[3][0]*self.balance*-1)
            
        elif particle[2][0] < radius:
            particle[2][0] = radius ; particle[3][0] = round(abs(particle[3][0]*self.balance))


    def touching(self, main_particle, main_particle_index, r):
        c  = 0
        mp_x, mp_y = main_particle[2][0] * self.m_to_pix,  main_particle[2][1] * self.m_to_pix
        for particle_index in range(self.number):
            if particle_index != main_particle_index:
                
                tp_x, tp_y = self.x[particle_index] * self.m_to_pix, self.y[particle_index] * self.m_to_pix

                ex, ey = mp_x - tp_x, mp_y - tp_y
                d = round(distance(ex, ey))
                if d < (r*2)+1:
                    c += 1
                    tex = ex/4
                    tey = ey/4

                    self.x[particle_index] += -1 * touchHitBox * tex / self.m_to_pix
                    main_particle[2][0] += touchHitBox * tex / self.m_to_pix
                    self.y[particle_index] += -1 * touchHitBox * tey / self.m_to_pix
                    main_particle[2][1] += touchHitBox * tey / self.m_to_pix

                    main_particle[3][0] = (-1 * main_particle[3][0]) * self.balance / self.m_to_pix
                    main_particle[3][1] = (-1 * main_particle[3][1]) * self.balance / self.m_to_pix 
                    self.speedX[particle_index] = (-1 * self.speedX[particle_index]) * self.balance / self.m_to_pix
                    self.speedY[particle_index] = (-1 * self.speedY[particle_index]) * self.balance / self.m_to_pix
                    
        return c



class physics:
    def __init__(self):
        self.gravity = 9.8
        self.m_to_pix = 110
        self.air_density = 1.225
    
    def air_ressistance(self, r, v):
        A = (r**2)*3.14
        Fd = A * self.air_density * v
        return Fd
        
        
        
        
        
        
        
        
        
                