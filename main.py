""" A very simple illustration of Darwinian evolution """

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from parts import Gen

prb = sys.argv[1] if sys.argv[1:] else 0
try: prb = float(prb)
except ValueError:
    print("Argument must be float",file=sys.stderr)
    sys.exit(1)

#######################################################
############### To be modified by user ################
#######################################################
M,N = 400,400

fitness=[1,1.1,1.1,1.2,1.1,0,0,0,1.1,0,0,0,1.2,0,0,1.3]

mu,recom = (
        1e-7,
        1e-4)

vmax = len(fitness) - 1

initial = np.zeros((M,N),dtype="int64")
#######################################################
#######################################################
#######################################################

gen = Gen(mu,initial,fitness,recom,prb)

fig = plt.figure(figsize=(8,8))
ax = fig.add_axes([0,0,1,1])
img = ax.imshow(initial,vmin=0,vmax=vmax)

def makeframe(state):
    img.set_data(state)
    return [img]

ani = FuncAnimation(fig,makeframe,gen,interval=50,
        blit=True)
        
plt.show()
