import numpy as np 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy import sin,cos,tan,arcsin,arccos,arctan,arctan2,sqrt,pi
#~ %matplotlib inline

def dh(a,alpha,d,theta):
    M = np.array([[cos(theta),-sin(theta)*cos(alpha),sin(theta)*sin(alpha),a*cos(theta)],
                  [sin(theta),cos(theta)*cos(alpha),-cos(theta)*sin(alpha),a*sin(theta)],
                  [0,sin(alpha),cos(alpha),d],
                  [0,0,0,1]])
    return M

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection='3d')

# IK
x,y,z = 2,1,1
d1,l2,l3 = 1,2,2
t1 = arctan2(y,x)
K1 = (x**2 + y**2 + z**2 - 2*d1*z + d1**2 - l2**2 - l3**2)/(2*l2*l3)
t3 = arctan2(sqrt(1-K1**2),K1)
s,r = (z-d1),sqrt(x**2+y**2)
t2 = arctan2(s*l2 + s*l3*cos(t3) - r*l3*sin(t3), r*l2 + r*l3*cos(t3) + s*l3*sin(t3))

# FK
T1_0 = dh(0,pi/2,d1,t1)
T2_1 = dh(l2,0,0,t2)
T3_2 = dh(l3,0,0,t3)
T2_0 = np.dot(T1_0,T2_1)
T3_0 = np.dot(T2_0,T3_2)
A = np.array([T1_0[0][3],T1_0[1][3],T1_0[2][3]])
B = np.array([T2_0[0][3],T2_0[1][3],T2_0[2][3]])
C = np.array([T3_0[0][3],T3_0[1][3],T3_0[2][3]])
ax.plot([0,A[0],B[0],C[0]],[0,A[1],B[1],C[1]],[0,A[2],B[2],C[2]],'-o')
plt.axis('equal')
plt.show()

