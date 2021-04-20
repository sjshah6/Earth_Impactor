# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 14:58:38 2021

@author: shirl
"""
import spiceypy as sp 
import numpy as np
import matplotlib.pyplot as plt 

def rad(a):
    r = a * np.pi/180
    return r
e = .08931408526295595	#eccentricity 
a = .9101475796007148 #semi major axis
i = rad(11.60890837462871)	#inclination 
Om = rad(146.9287251666387)	#Right Ascension of Node
w = rad(195.5640381628273) #Argument of periapse
M = rad(168.6650218763381)	#mean anomaly
epoch = 400
et = 0
Gm = 0.01720209895**2
elts = [a, e, i, Om, w, M, epoch, Gm]
state = sp.conics(elts, et)
print(state)
et1 = 300
et1 = np.arange(1, 1e6, 10)
final = []
for t in et1:
    final.append(sp.prop2b(Gm, state, t))
final = np.array(final)
fig = plt.figure()

ax = plt.axes(projection = '3d')
ax.plot(final[:,0], final[:,1], final[:,2], color = 'rebeccapurple')
plt.figure(figsize = (4,4) )
plt.plot(final[:,0], final[:,1], color = 'rebeccapurple')
