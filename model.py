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

        
#parameters of simulation
#la duree de retard de visibilite
h=1
#le debit de transaction arrivant par unite de temps
poisson_par=3
#le parametre utilise par l'algorithme BRW permettant de calculer les probabilites
#de transition dans le graphe
alpha=0.001
#le pas de la simulation
pas=0.5
#la duree total de la simulation
total_time=50
#coefficient de division utilisateur (ex 1/3 => 1/3 utilisateurs, 2/3 de l'autre)
coef_div = 1/12
#l'algorithme de selection choisi
algo="BRW"
#le nombre d'utilisateur
nb_user = 100
#le temps du split
partition_time = 10
#le temps de la jonction
join_time = 30

parameters = {'h':h,'rate':poisson_par,'alpha':alpha,'pas':pas,'total time':total_time,'coef div':coef_div,'algo':"BRW",}

#simulation
simulation = SimulationSplit(pas,total_time, poisson_par,h , 10, coef_div,100, "BRW")

duree=time()
simulation.simulate_split(30)
duree=time()-duree

print("duree de la simulation:{}".format(duree))


plt.show()