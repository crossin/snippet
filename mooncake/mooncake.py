import numpy as np
from numpy import sin, cos, pi
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
from matplotlib.patches import Arc, Circle, Wedge
from matplotlib.collections import PatchCollection

length = 20
R = 3**0.5*length/(3**0.5*cos(pi/12)-sin(pi/12))
r = 2*sin(pi/12)*R/3**0.5

arc1 = Arc([0, length], width=2*r, height=2*r, angle=0, theta1=30, theta2=150, ec='orange', linewidth=4)
arc2 = Arc([-length/2, length/2*3**0.5], width=2*r, height=2*r, angle=0, theta1=60, theta2=180, ec='orange', linewidth=4)
arc3 = Arc([-length/2*3**0.5, length/2], width=2*r, height=2*r, angle=0, theta1=90, theta2=210, ec='orange', linewidth=4)
arc4 = Arc([-length, 0], width=2*r, height=2*r, angle=0, theta1=120, theta2=240, ec='orange', linewidth=4)
arc5 = Arc([-length/2*3**0.5, -length/2], width=2*r, height=2*r, angle=0, theta1=150, theta2=270, ec='orange', linewidth=4)
arc6 = Arc([-length/2, -length/2*3**0.5], width=2*r, height=2*r, angle=0, theta1=180, theta2=300, ec='orange', linewidth=4)
arc7 = Arc([0, -length], width=2*r, height=2*r, angle=0, theta1=210, theta2=330, ec='orange', linewidth=4)
arc8 = Arc([length/2, -length/2*3**0.5], width=2*r, height=2*r, angle=0, theta1=240, theta2=360, ec='orange', linewidth=4)
arc9 = Arc([length/2*3**0.5, -length/2], width=2*r, height=2*r, angle=0, theta1=270, theta2=390, ec='orange', linewidth=4)
arc10 = Arc([length, 0], width=2*r, height=2*r, angle=0, theta1=300, theta2=420, ec='orange', linewidth=4)
arc11 = Arc([length/2*3**0.5, length/2], width=2*r, height=2*r, angle=0, theta1=330, theta2=450, ec='orange', linewidth=4)
arc12 = Arc([length/2, length/2*3**0.5], width=2*r, height=2*r, angle=0, theta1=0, theta2=120, ec='orange', linewidth=4)

art_list = [arc1, arc2, arc3, arc4, arc5, arc6, arc7, arc8, arc9, arc10, arc11, arc12]

circle = Circle((0,0), R, ec='orange', fc='white', linewidth=4)

wedge1 = Wedge([-2, 2], R-5, 90, 180, ec='orange', fc=r'white', linewidth=4)
wedge2 = Wedge([-5, 5], R-12, 90, 180, ec='orange', fc=r'white', linewidth=4)
wedge3 = Wedge([-2, -2], R-5, 180, 270, ec='orange', fc=r'white', linewidth=4)
wedge4 = Wedge([-5, -5], R-12, 180, 270, ec='orange', fc=r'white', linewidth=4)
wedge5 = Wedge([2, -2], R-5, 270, 360, ec='orange', fc=r'white', linewidth=4)
wedge6 = Wedge([5, -5], R-12, 270, 360, ec='orange', fc=r'white', linewidth=4)
wedge7 = Wedge([2, 2], R-5, 0, 90, ec='orange', fc=r'white', linewidth=4)
wedge8 = Wedge([5, 5], R-12, 0, 90, ec='orange', fc=r'white', linewidth=4)

art_list.extend([circle, wedge1, wedge2, wedge3, wedge4, wedge5, wedge6, wedge7, wedge8])
fig, ax = plt.subplots(figsize=(8,8))
ax.set_aspect('equal')
for a in art_list:
    ax.add_patch(a)

plt.text(-18, -2.5, 'CROSSIN', fontfamily=r'Times New Man', bbox=dict(boxstyle='square', fc="w", ec='orange', linewidth=4),  fontsize=50, color='orange')

plt.ylim([-35, 35])
plt.xlim([-35, 35])

plt.show()

