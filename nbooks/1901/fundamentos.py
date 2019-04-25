from sympy import *
from sympy.matrices import *
import matplotlib.pyplot as plt
import numpy as np
init_printing()

t1,t2,t3,t4,t5,t6 = symbols("\\theta_1:7")
d1,d2,d3,d4,d5,d6 = symbols("d_1:7")
l1,l2,l3,l4,l5,l6 = symbols("l_1:7")

def rotz(theta):
    H = Matrix([[cos(theta), -sin(theta), 0, 0], 
                [sin(theta), cos(theta), 0, 0], 
                [0,0,1,0],
                [0,0,0,1]])
    return H

def roty(theta):
    H = Matrix([[cos(theta), 0, sin(theta), 0], 
                [0,1,0,0],
                [-sin(theta), 0, cos(theta), 0], 
                [0,0,0,1]])
    return H

def rotx(theta):
    H = Matrix([[1,0,0,0],
                [0, cos(theta), -sin(theta), 0], 
                [0, sin(theta), cos(theta), 0], 
                [0,0,0,1]])
    return H

def Dx(d):
    H = Matrix([[1, 0, 0, d], 
               [0, 1, 0, 0], 
               [0, 0, 1, 0],
               [0, 0, 0, 1]])
    return H

def Dy(d):
    H = Matrix([[1, 0, 0, 0], 
               [0, 1, 0, d], 
               [0, 0, 1, 0],
               [0, 0, 0, 1]])
    return H

def Dz(d):
    H = Matrix([[1, 0, 0, 0], 
               [0, 1, 0, 0], 
               [0, 0, 1, d],
               [0, 0, 0, 1]])
    return H

def dh(a, alpha, d, theta):
    ct = cos(theta)
    st = sin(theta)
    ca = cos(alpha)
    sa = sin(alpha)
    H = Matrix([[ct, -st*ca, st*sa, a*ct], 
                [st, ct*ca, -ct*sa, a*st],
                [0, sa, ca, d],
                [0, 0, 0, 1]])
    return H

l1,l2 = 300,300
Px,Py = 300,500
t2 = acos( (Px**2 + Py**2 - l1**2 - l2**2) / (2*l1*l2) )
t2eu = -t2
t1 = atan2( Py*l1 + Py*l2*cos(t2) - Px*l2*sin(t2), Px*l1 + Px*l2*cos(t2) + Py*l2*sin(t2) )
t1eu = atan2( Py*l1 + Py*l2*cos(t2eu) - Px*l2*sin(t2eu), Px*l1 + Px*l2*cos(t2eu) + Py*l2*sin(t2eu) )
plt.plot([0, l1*cos(t1), l1*cos(t1) + l2*cos(t1+t2)], 
         [0, l1*sin(t1), l1*sin(t1) + l2*sin(t1+t2)], "r-o")
plt.plot([0, l1*cos(t1eu), l1*cos(t1eu) + l2*cos(t1eu+t2eu)], 
         [0, l1*sin(t1eu), l1*sin(t1eu) + l2*sin(t1eu+t2eu)], "b-o")
plt.grid(ls="--");
plt.axis("square");
plt.show()