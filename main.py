# Parameters to be modified by user as he sees fit

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from parts import *

M,N = 400,400
fitness = [ 
        #0
        1,
        #1
        1.1,
        #2
        1.1,
        #3
        1.2,
        #4
        1.1,
        #5
        0,
        #6
        0,
        #7
        0,
        #8
        1.1,
        #9
        0,
        #10
        0,
        #11
        0,
        #12
        1.2,
        #13
        0,
        #14
        0,
        #15
        1.3]

initial = np.zeros((M,N),dtype="int64")

mu,L,recom = (
        1e-7,
        4,
        1e-4)

gen = Gen(mu,initial,L,fitness,recom)

fig = plt.figure(figsize=(8,8))
ax = fig.add_axes([0,0,1,1])
img = ax.imshow(initial,vmin=0,vmax=15)

def makeframe(state):
    img.set_data(state)
    return [img]

ani = FuncAnimation(fig,makeframe,gen,interval=50,
        blit=True)
        
plt.show()
