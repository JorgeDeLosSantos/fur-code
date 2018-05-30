# License: MIT License
# Author: Pedro Jorge De Los Santos
# E-mail: delossantosmfq@gmail.com
from furlib import *
from numpy import pi
import numpy as np
from mpl_toolkits.mplot3d import  axes3d,Axes3D
import scipy as sp
from scipy.spatial import ConvexHull

r = Manipulator((20,pi/2,80,t1),(100,0,0,t2),(100,0,0,t3))
T = r.T
px = T[0,3]
py = T[1,3]
pz = T[2,3]
X,Y,Z = [],[],[]
for T1 in np.linspace(-pi/2, pi/2, 50):
    for T2 in np.linspace(-pi/2, pi/2, 50):
        for T3 in np.linspace(-pi/2, pi/2, 50):
            X.append(float(px.subs({t1:T1, t2:T2, t3:T3})))
            Y.append(float(py.subs({t1:T1, t2:T2, t3:T3})))
            Z.append(float(pz.subs({t1:T1, t2:T2, t3:T3})))

fig = plt.figure()
ax = fig.gca(projection='3d')

V = np.array([X,Y,Z]).T
hull = ConvexHull(V)
#~ ax.plot(V[:,0], V[:,1], V[:,2], '.')
for simplex in hull.simplices:
    simplex = np.append(simplex, [simplex[0]])
    #~ print(V[simplex, 0])
    try:
        ax.plot_trisurf(V[simplex, 0], V[simplex, 1], V[simplex, 2], color="#FF00FF77",edgecolor='#AAAAAA')
    except:
        pass

plt.show()
#r.plot_diagram({t1:0, t2:0, t3:0})
#plt.show()
