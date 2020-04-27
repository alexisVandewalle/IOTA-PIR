class User:
    def __init__(self, id,wallet):
        self.wallet = wallet
        self.id = id
    
    def __str__(self):
        return "l'utilisateur {} possede {} pieces".format(self.id, self.wallet)
        

class MasterUser(User):
    def __init__(self):
        User.__init__(self,0,0)
