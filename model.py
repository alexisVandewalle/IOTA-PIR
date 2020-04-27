#importations
import networkx as nx
import matplotlib.pyplot as plt
import random as rd
import numpy as np
from time import time
from user import *
from tangle import *
from simulation import *
from transaction import *
from settings import *

#simulation
simulation = SimulationSplit()

duree=time()
simulation.simulate()
duree=time()-duree

print("duree de la simulation:{}".format(duree))


plt.show()