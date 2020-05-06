import networkx as nx
import matplotlib.pyplot as plt
import random as rd
import numpy as np
from user import *
from transaction import *
from settings import parameters



class Tangle:
    """
    Cette classe permet de représenter le tangle, graphe qui contient l'ensemble
    des transactions
    """
    
    def __init__(self, users):
        """
        Cette fonction créé le tangle en créant une transaction racine
        """
        self.genesis = Genesis(MasterUser())
        self.G=nx.DiGraph()
        self.G.add_node(self.genesis)
        self.graph_path=nx.DiGraph()
        self.graph_path.add_node(self.genesis)
        self.users = users


    def is_tips(self,node,actual_time):
        list_neighbors=list(self.graph_path[node])
        for neighbor in list_neighbors:
            if neighbor.is_visible(actual_time):
                return False
        return True


    def remove_branch(self, node,actual_time):

        node_to_visit = [node]
        visited_node = dict()
        visited_node[node] = None

        while len(node_to_visit) != 0:
            current_node = node_to_visit.pop(0)
            list_neighbor = self.graph_path[current_node]
            for neighbor in list_neighbor:
                if neighbor in visited_node:
                    pass
                else:
                    node_to_visit.append(neighbor)
                    visited_node[neighbor] = None
                    neighbor.sender.wallet.append((actual_time,neighbor.sender.wallet[-1][1]+neighbor.montant))
                    neighbor.receiver.wallet.append((actual_time,neighbor.receiver.wallet[-1][1]-neighbor.montant))
        
        self.G.remove_nodes_from(visited_node)
        self.graph_path.remove_nodes_from(visited_node)
        


    def check_transactions(self, time):
        wrong_node = []
        for node in self.G:
            if node.check_transaction(time) == False:
                wrong_node.append(node)

        for node in wrong_node:
            if node in self.G: #le fait d'enlever des branches peut enlever d'autres noeuds
                self.remove_branch(node,time)

    def copy(tangle,users):
        new = Tangle(users)
        new.genesis = tangle.genesis
        new.G = tangle.G.copy()
        new.graph_path = tangle.graph_path.copy()
        new.users = users
        return new


    def get_visible_tips(self,actual_time):
        """
        Cette fonction permet de récupérer tous les tips visible à un instant
        donné
        actual_time: le temps actuel de la simulation
        return     : la liste des tips visible par l'ensemble du reseau
        """
        
        tips_list=[]
        for node in self.G:
            if self.is_tips(node,actual_time):
                tips_list.append(node)
        return tips_list
    
    
    def get_visible_neighbors(self,node, actual_time):
        """
        Cette fonction permet de récupérer les voisins visible d'un noeud
        actual_time: le temps actuel de la simulation
        node       : le noeud considere
        return     : la liste des voisins visibles par ce noeud
        """
        
        list_neighbors=list(self.graph_path[node])
        result=[]
        for neighbor in list_neighbors:
            if neighbor.is_visible(actual_time):
                result.append(neighbor)
        return result
        
        
    def compute_cumulative_weight(self,node,actual_time):
        """
        Cette fonction calcule le poids cumule d'un noeud a un instant donne
        node       : le noeud considere
        actual_time: le temps actuel de la simulation
        """
        
        node_to_visit=[node]
        possible_node=dict()
        possible_node[node]=None
        
        while len(node_to_visit)!=0:
            current_node=node_to_visit.pop(0)
            list_neighbor = self.get_visible_neighbors(current_node,actual_time)
            for neighbor in list_neighbor:
                if neighbor in possible_node:
                    pass
                else:
                    node_to_visit.append(neighbor)
                    possible_node[neighbor]=None
        node.cumulative_weight=len(possible_node)
    
    
    def computeGlobalWeight(self,actual_time):
        """
        Cette fonction permet de calculer l'ensemble des poids cumule a un instant
        donne.
        actual_time: le temps actuel de la simulation
        """
        
        for node in self.G:
            self.compute_cumulative_weight(node,actual_time)
         
                
    def URW(self,actual_time):
        """
        Cette fonction selectionne un tips visible dans le tangle en realisant
        une marche aleatoire uniforme sur l'ensemble du tangle.
        actual_time : le temps actuel de la simulation
        return      : le tips qui a ete selectionne 
        """
        
        current_node=self.genesis
        while not self.is_tips(current_node,actual_time):
            list_neighbor=self.get_visible_neighbors(current_node,actual_time)
            N=len(list_neighbor)
            rd_index=rd.randint(0,N-1)
            current_node=list_neighbor[rd_index]
        
        return current_node
    

    def BRW(self,actual_time):
        """
        Cette fonction selectionne un tips visible dans le tangle en realisant
        une marche aleatoire biaisee (Biased Random Walk) sur l'ensemble du 
        tangle
        actual_time : le temps actuel de la simulation
        return      : le tips qui a ete selectionne 
        """
        
        current_node=self.genesis

        while not self.is_tips(current_node,actual_time):
            list_neighbor=self.get_visible_neighbors(current_node,actual_time)
            list_weight=[0]
            sum=0
            for neighbor in list_neighbor:
                list_weight.append(np.exp(parameters['alpha']*neighbor.cumulative_weight)+sum)
                sum += np.exp(parameters['alpha']*neighbor.cumulative_weight)
                
            list_weight = np.array(list_weight)
            list_weight=1/list_weight[-1]*list_weight
            
            rd_number=rd.random()
            
            for i in range(len(list_weight)-1):
                if list_weight[i]<=rd_number and list_weight[i+1]>rd_number:
                    index=i
                    break
            
            current_node=list_neighbor[index]
        return current_node

    
    def simulate_one_step(self,actual_time,n_branche=0):
        """
        Cette fonction simule un pas de temps de la simulation
        actual_time: le temps actuel de la simulation
        pas        : le pas de la simulation
        algo       : l'algorithme choisi valant "BRW" ou "URW" 
        """


        if(parameters['algo']=="BRW"):
            self.computeGlobalWeight(actual_time)

        number_of_transactions = np.random.poisson(parameters['rate']*parameters['pas'])
        transactions = [Transaction(actual_time,rd.sample(self.users,2),rd.random()*10,n_branche) for i in range(number_of_transactions)]
        for t in transactions:
            while True:
                if(parameters['algo']=="BRW"):
                    t1=self.BRW(actual_time)
                    t2=self.BRW(actual_time)
                    
            
                elif(parameters['algo']=="URW"):
                    t1=self.URW(actual_time)
                    t2=self.URW(actual_time)

                if t1.check(actual_time) and t2.check(actual_time):
                    break


            self.G.add_node(t)
            self.graph_path.add_node(t)
            self.G.add_edge(t,t1)
            self.G.add_edge(t,t2)
            self.graph_path.add_edge(t1,t)
            self.graph_path.add_edge(t2,t)
        
    def split(tangle, users1, users2):
        tangle1 = Tangle.copy(tangle,users1)
        tangle2 = tangle
        tangle2.users = users2
        return tangle1,tangle2
        
    def join(tangle1, tangle2):
        tangle1.users = tangle1.users + tangle2.users
        tangle1.G.add_edges_from(tangle2.G.edges)
        tangle1.graph_path.add_edges_from(tangle2.graph_path.edges)
        return tangle1

    def display(self):
        """
        affiche l'ensemble du tangle.
        """
        self.computeGlobalWeight(parameters['total time']+2*parameters['h'])
        position=dict()
        size=[]
        color=[]
        count=0
        coef = 1/self.genesis.cumulative_weight*600

        for node in self.G:
            if(node == self.genesis):
                position[node]=(node.created_time,(parameters['rate']*parameters['pas'])/2)

            else:
                position[node]=(node.created_time, count%(parameters['rate']*parameters['pas'])+node.n_branche*parameters['rate']*parameters['pas'])

            size.append(node.cumulative_weight*coef)
            if self.is_tips(node,parameters['total time']+2*parameters['h']):
                color.append('red')
            else:
                color.append('blue')

            count+=1

        nx.draw_networkx(self.G,position,node_size=size,node_color=color,node_shape='s')
        plt.xlabel("time")
        plt.grid(True, linestyle='--')