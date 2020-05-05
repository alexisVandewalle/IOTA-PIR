from collections import OrderedDict
from settings import parameters

class User:
    def __init__(self, id,wallet,created_time=0):
        self.wallet = [(created_time,wallet)]
        self.id = id

    def __str__(self):
        return "l'utilisateur {} possede {} pieces".format(self.id, self.wallet)
        

class MasterUser(User):
    def __init__(self):
        User.__init__(self,0,0,-2*parameters['h'])
