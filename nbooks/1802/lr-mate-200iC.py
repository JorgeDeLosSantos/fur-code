# License: MIT License
# Author: Pedro Jorge De Los Santos
# E-mail: delossantosmfq@gmail.com
from furlib import *
import numpy as np 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

Fanuc = Robot((75,-pi/2,330,t1), (300,pi,0,t2), (75,-pi/2,0,t3), (0,pi/2,-320,t4), (0,-pi/2,0,t5), (0,pi,-80,t6))
#T = Fanuc.T

deg = lambda x: (x*180/pi).evalf()
rad = lambda x: (x*pi/180).evalf()

phi,theta,psi = 0,pi,0
H = ea2htm(phi,theta,psi)
a1,d1,a2,a3,d4,d6 = 75,330,300,75,320,80
x,y,z = 300,200,200

xm,ym,zm = x - d6*H[0,2], y - d6*H[1,2], z - d6*H[2,2]
T1 = atan2(ym,xm).evalf(chop=True)
b = sqrt(xm**2 + ym**2)
a = zm - d1
c = sqrt(a**2 + (b-a1)**2)
d = sqrt(a3**2 + d4**2)
beta = atan2(a, b-a1)
K1 = (a2**2+c**2-d**2)/(2*a2*c)
alpha = atan2(sqrt(1-K1**2), K1)
K2 = (a2**2+d**2-c**2)/(2*a2*d)
gamma = atan2(sqrt(1-K2**2), K2)
delta = atan2(d4,a3)

T2 = -(alpha + beta).evalf(chop=True)
T3 = (gamma + delta - pi).evalf(chop=True)

# Orientación

R3_0 = ( dhs(75,-pi/2,330,T1)*dhs(300,pi,0,T2)*dhs(75,-pi/2,0,T3) )[:3,:3]
R6_0 = H[:3,:3]
R6_3 = R3_0.inv()*R6_0
T4 = atan2(R6_3[1,2], R6_3[0,2]).evalf(chop=True)
K5 = -R6_3[2,2]
T5 = atan2(sqrt(1-K5**2),K5).evalf(chop=True)
T6 = atan2(R6_3[2,1], R6_3[2,0]).evalf(chop=True)

for ang in (T1,T2,T3,T4,T5,T6):
    print(deg(ang))
    
vals = {t1:T1,t2:T2,t3:T3,t4:T4,t5:T5,t6:T6}

Fanuc.plot_diagram(vals)
plt.show()


