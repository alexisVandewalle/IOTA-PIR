#importations
from time import time
from simulation import *


#simulation
simulation = SimulationSplit()

duree=time()
tangle = simulation.simulate()
duree=time()-duree

print("duree de la simulation:{}".format(duree))


plt.show()