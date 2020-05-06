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
        self.is_check = False
        
    def check(self, actual_time):
        if not self.is_check:
            swallet = self.sender.wallet[-1][1]
            rwallet = self.receiver.wallet[-1][1]
            if swallet - self.montant >= 0:
                self.sender.wallet.append((actual_time, swallet - self.montant))
                self.receiver.wallet.append((actual_time, rwallet + self.montant))
                self.is_check = True
                return True
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
        return "{}".format(self.cumulative_weight)
        

class Genesis(Transaction):
    def __init__(self,masterUser):
        Transaction.__init__(self,-2*parameters['h'],[masterUser,masterUser])
        # self.actualise_wallet(-2*parameters['h'])