from settings import parameters

class Transaction:
    """Cette classe permet de definir un objet transaction, c'est à dire un noeud
    du tangle"""
    
    def __init__(self,created_time,list_s_r, montant=0,n_branche=0):
        """
        created_time: le temps auquel est cree la transaction
        visible:      permet de dire si la transaction est visible par l'ensemble
        du tangle ou non
        """
        
        self.sender = list_s_r[0]
        self.receiver = list_s_r[1]
        self.montant = montant
        self.cumulative_weight=1
        self.created_time = created_time
        self.n_branche = n_branche
        self.confidence_rate =0

    def check(t1,t2, tangle):
        """
        Cette fonction vérifie si deux transactions sont valides ou non.
        Pour cela, la fonction recense toutes les transactions indirectement validé par les deux transactions, puis
        vérifie que tous les utilisateurs possède bien un porte monnaie positif. Si ce n'est pas le cas, la fonction
        , il y a un conflit dans l'arbre et la fonction renvoie false.
        :param t1: transaction 1
        :param t2: transaction 2
        :param tangle: le tangle
        :return:
        """
        node_to_visit = [t1,t2]
        visited_node = dict()
        visited_node[t1] = None
        visited_node[t2] = None
        while len(node_to_visit) != 0:
            current_node = node_to_visit.pop(0)
            neighbors = list(tangle.G[current_node])
            for neighbor in neighbors:
                if not(neighbor in visited_node):
                    node_to_visit.append(neighbor)
                    visited_node[neighbor] = None

        users_wallet = dict()
        users_wallet[tangle.genesis.sender] = 0

        for t in visited_node:
            if t.sender in users_wallet:
                users_wallet[t.sender]-=t.montant
            else:
                users_wallet[t.sender] = parameters['init wallet'] - t.montant

            if t.receiver in users_wallet:
                users_wallet[t.receiver]+=t.montant
            else:
                users_wallet[t.receiver] = parameters['init wallet'] + t.montant

            if users_wallet[t.sender]<0:
                return False
        return True


    def is_visible(self,time):
        """
        Cette fonction permet de savoir si une transaction est visible a un
        instant donne et actualise sa visibilite si necessaire
        time: le temps actuel de la simulation
        return: True si la transaction est visible, False sinon
        """

        if(self.created_time<time-parameters['h']):
            return True
        else:
            return False

    def __str__(self):
        """
        Cette fonction retourne une chaine de caracteres contenant le poids 
        cumule de la transaction
        """
        return "{:.2f}".format(self.confidence_rate)
        

class Genesis(Transaction):
    def __init__(self,masterUser):
        Transaction.__init__(self,-2*parameters['h'],[masterUser,masterUser])
        # self.actualise_wallet(-2*parameters['h'])