# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 10:12:02 2021

@author: shirl
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import spiceypy as sp
from Conversions import *
from jplephem.spk import SPK
import scipy as sc 
from scipy import optimize
import csv
from random import random 



Gm = 0.01720209895**2 #Gaussian Gravitational Constant 
r_earth = 6378 #radius of earth in km  
r_earth_au = .0000426352 #radius in au
df = pd.read_csv("earth_impactors.csv") #read csv file
sp.furnsh('EarthImpactor.txt') #load kernels
column_names = ['Date', 'a[au]', 'e[]', 'i[rad]', 'node[rad]', 'omega[rad]', 'mA[rad]']


utc = ['Jan 1, 2025', 'Dec 31,2025']
FirstDay = sp.str2et(utc[0])
LastDay = sp.str2et(utc[1])
with open('new_earth_impactors.csv','w' ,newline ='' ) as file:
     writer= csv.writer(file)
     writer.writerow(column_names)

for i in range(100):
    
    time = getEarthTime(rad(gfd(i, 'trueAnomaly1[deg]', df)))
    T0 = time+FirstDay
    JD_Time_earth = sp.et2utc(time+FirstDay, 'J', 14) #Julian Date at this particular true anmoly 
    C_Time_earth = sp.et2utc(time+FirstDay, 'C', 14)
    #print(JD_Time) #Time where the earth is at the specifie
    pos_vel_earth = convertEarth(sp.spkezr('EARTH',time+FirstDay, 'J2000', 'LT+S', 'SUN' )) #will find the position and velocity of earth at specific ephermeris w/ respect to the sun
    pos_vel_km = sp.spkezr('EARTH',time+FirstDay, 'J2000', 'LT+S', 'SUN' )
    
      
   
    
    et = 0
    a = gfd(i, ' a[au]', df)*1.496e+8
    e = gfd(i, 'e[]', df)
    inc = rad(gfd(i, 'i[deg]', df))
    node = rad(gfd(i, 'node[deg]', df))
    omega = rad(gfd(i, 'w[deg]', df))
    M_A = toMean(rad(gfd(i, 'trueAnomaly2[deg]',df)), e)
    elts_ast = np.array([a, e, inc, node, omega, M_A, et, Gm])
    opt1 = sc.optimize.minimize(dist, [T0, rad(gfd(i, 'trueAnomaly2[deg]',df))], args=(elts_ast, Gm ), method = 'CG')
    opt2 = sc.optimize.minimize(dist1, [node, omega, opt1.x[0],opt1.x[1]], args=(elts_ast, Gm), method = 'CG')
    print(opt2.x)
    new_mean= toMean(opt2.x[3], e)
    new_elts_ast = np.array([a, e, inc, opt2.x[0], opt2.x[1], new_mean, et, Gm])
    new_pos_ast = convertAst(sp.conics(new_elts_ast, 0))
    new_earth_pos = convertEarth(sp.spkezr('EARTH',opt2.x[2], 'J2000', 'LT+S', 'SUN' ))
    distance = np.linalg.norm(new_earth_pos[0:3] - new_pos_ast[0:3])
    #print(distance)
    
    if distance > r_earth:
        new_elts_ast = sp.oscelt(correction(new_earth_pos-new_pos_ast), T0,Gm)
    final_data = [C_Time_earth, new_elts_ast[0]*6.6846e-9,new_elts_ast[1],new_elts_ast[2],new_elts_ast[3],new_elts_ast[4],new_elts_ast[5]]
    with open('new_earth_impactors.csv','a' ,newline ='' ) as file:
     writer= csv.writer(file)
     writer.writerow(final_data)

        
                                 
                                 
                                 
                                 
    #print(new_elts_ast[0]*)
    

                          
# with open('new_earth_impactors.csv','w' ,newline ='' ) as file:
#     writer= csv.writer(file)
#  writer.writerow
