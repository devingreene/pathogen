""" A very simple illustration of Darwinian evolution """

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from parts import Gen
from lexorder import lex2num,num2lex
from utils import bitlength

#######################################################
############### To be modified by user ################
#######################################################
M,N = 400,400

fitness=[1,
        1.1,1.1,1.1,1.1,
        1.2,0,0,0,0,1.2,
        0,0,0,0,
        1.3]

# Convert to numerical order
fitness = lex2num(fitness)

nloci = bitlength(len(fitness))

mu,recom = (
        1e-7,
        1e-4)

vmax = len(fitness) - 1

initial = np.zeros((M,N),dtype="int64")

exposure_rate = 0.3

migration_rate = 0.0001
#######################################################
#######################################################
#######################################################

plt.rcParams.update({'font.family':'monospace'})

gen = Gen(mu,initial,fitness,recom,exposure_rate,migration_rate)

fig = plt.figure(figsize=(7,6),frameon=False)
ax_main = fig.add_subplot(121,position = [0,0,6/7,1],frameon=False,yticks=[])
ax_lab = fig.add_subplot(122,position = [6/7,0,1/7,1],frameon=False,yticks=[])
img = ax_main.imshow(initial,
        vmin=0,
        vmax=vmax,
        cmap = "YlOrRd",
        aspect='auto')

lex = num2lex(list(range(len(fitness))))
sm = mpl.cm.ScalarMappable(cmap=img.get_cmap())
sm.set_clim(0,vmax)

for i,l in enumerate(lex):
    ax_lab.text(1/2,0.95 - 0.035*i,"{:0{:d}b}".format(l,nloci),
            ha="center",va="center",
            backgroundcolor=sm.to_rgba(l))

def makeframe(state):
    img.set_data(state)
    return [img]

ani = FuncAnimation(fig,makeframe,gen,interval=50,
        blit=True)
plt.show()
