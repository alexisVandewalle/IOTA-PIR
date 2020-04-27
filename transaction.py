

class Transaction:
    """Cette classe permet de definir un objet transaction, c'est à dire un noeud
    du tangle"""
    
    def __init__(self,created_time,list_s_r,h, montant=0,n_branche=0):
        """
        created_time: le temps auquel est cree la transaction
        visible:      permet de dire si la transaction est visible par l'ensemble
        du tangle ou non
        """
        
        self.sender = list_s_r[0]
        self.receiver = list_s_r[1]
        self.montant = montant
        self.cumulative_weight=1
        self.created_time=created_time
        self.tips=True
        self.n_branche = n_branche
        self.h = h
        
    def actualise_wallet(self):
        self.sender.wallet -= self.montant
        self.receiver.wallet += self.montant
    
    def is_visible(self,time):
        """
        Cette fonction permet de savoir si une transaction est visible a un
        instant donne et actualise sa visibilite si necessaire
        time: le temps actuel de la simulation
        return: True si la transaction est visible, False sinon
        """

        if(self.created_time<time-self.h):
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
    def __init__(self,masterUser,h):
        Transaction.__init__(self,-2*h,[masterUser,masterUser],h,0)