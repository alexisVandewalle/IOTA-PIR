from collections import OrderedDict
from settings import parameters

class User:
    def __init__(self, id,init_wallet):
        self.init_wallet = init_wallet
        self.id = id

    def __str__(self):
        return "l'utilisateur {} possede initialement {} pieces".format(self.id, self.wallet)
        

class MasterUser(User):
    def __init__(self):
        User.__init__(self,0,0)
