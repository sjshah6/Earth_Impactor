# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 11:08:44 2021

@author: shirl
"""

import spiceypy as sp 
import numpy as np
import matplotlib.pyplot as plt 
import math 
from random import random 

def rad(a):   #conversion to radians from degrees
    r = a * (np.pi/180)
    return r

def toMean(tA,e):    #true anomolay in radian 
    tanEY = (math.sqrt(1 - e**2)*np.sin(tA))
    tanEX = (e + np.cos(tA))
    E = np.arctan2(tanEY,tanEX)
    #y = math.tan(tA/2)
    #x = math.sqrt((1+e)/(1-e))
    #E = 2 * np.atan2(y, x)
    M = E - (e*np.sin(E))
    return M
def gfd(i, label, df):
    return df.iloc[i][label]
def convertEarth(a):
    
    pos1 = sp.convrt(a[0][0], 'KM', 'AU')
    pos2 =sp.convrt(a[0][1], 'KM', 'AU')
    pos3 = sp.convrt(a[0][2], 'KM', 'AU')
    vel1 = a[0][3]*(86400/149597870.700)
    vel2 = a[0][4]*(86400/149597870.700)
    vel3 = a[0][5]*(86400/149597870.700)
    return np.array([pos1, pos2, pos3,vel1,vel2,vel3])
def convertAst(a):
    
    pos1 = sp.convrt(a[0], 'KM', 'AU')
    pos2 =sp.convrt(a[1], 'KM', 'AU')
    pos3 = sp.convrt(a[2], 'KM', 'AU')
    vel1 = a[3]*(86400/149597870.700)
    vel2 = a[4]*(86400/149597870.700)
    vel3 = a[5]*(86400/149597870.700)
    return np.array([pos1, pos2, pos3,vel1,vel2,vel3])
def getEarthTime(tA):
    e_earth = 0.0167 #eccentricity of earth   
    n = 0.01720209895**2
    n_earth = (2*np.pi)/365 #which n to use?
    mean_o = toMean(tA, e_earth)
    #print(mean_o)
    return abs((mean_o/n)*24*60*60) #M = n*t
def dist(x, ele_ast,Gm):
    #x[0] is time and x[1] is true anomaly 
    M_A = toMean(x[1], ele_ast[1])
    pos_earth = sp.spkpos('EARTH',x[0], 'J2000', 'LT+S', 'SUN' )
    ele = np.zeros(8)
    ele[0:4]=ele_ast[0:4]
    ele[5]=M_A
    ele[6]=0
    ele[7]=Gm
    xyz_asteroid = sp.conics(ele, 0)[0:3]
    d = np.linalg.norm(pos_earth[1] - xyz_asteroid)
    return d
def dist1(x, ele_ast, Gm):
    #x[0] node, x[1] argp, x[2] time(earth), x[3] tA of asteroid 
    pos_earth = sp.spkpos('Earth', x[2], 'J2000', 'LT+S', 'SUN')
    ele = np.zeros(8)
    ele[0:2] = ele_ast[0:2]
    ele[3] = x[0]
    ele[4] = x[1]
    ele[5] = toMean(x[3], ele_ast[1])
    ele[6] = 0
    ele[7] = Gm 
    xyz_ast = sp.conics(ele, 0)[0:3]
    d = np.linalg.norm(pos_earth[1]-xyz_ast)
    return d
    

    #x[0] is omega, x[1] is node, x[2] is 
def correction(a): #takes position in 
    r_earth_au = 4.26352e-5 #radius in au
    r_earth = 6378
    value = random()
    mag = np.linalg.norm(a)
    new_mag = r_earth*value
    scale = new_mag/mag
    new_x = scale*a[0]
    new_y = scale*a[1]
    new_z = scale*a[2]
    a = np.array([new_x, new_y, new_z, a[3], a[4], a[5]])
    
    return a
    


