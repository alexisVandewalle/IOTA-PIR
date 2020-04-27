from user import *
from tangle import *
from transaction import *

#class
class Simulation:
    def __init__(self, pas, total_time, rate, h, nb_users=100, algo="BRW"):
        self.pas = pas
        self.total_time = total_time
        self.algo = algo
        self.users = [User(i+1,100) for i in range(nb_users)]
        self.tangle = Tangle(self.users, h)
        self.rate = rate
        self.h = h
        
    def simulate(self):
        number_of_step = int(self.total_time/self.pas)
        for i in range(number_of_step):
            self.tangle.simulate_one_step(self.h, self.pas*(i+1),self.pas,self.algo,self.rate)
        self.tangle.display()

        
class SimulationSplit(Simulation):
    
    def __init__(self, pas, total_time, rate, h,partition_time, coef_div=1/2, nb_users=100, algo="BRW"):
        Simulation.__init__(self, pas, total_time, rate, h, nb_users, algo)
        self.partition_time = partition_time
        self.coef_div = coef_div
        
        
    def simulate_split(self,join_time):
        number_of_step=int(self.total_time/self.pas)
        for i in range(int(self.partition_time/self.pas)):
            self.tangle.simulate_one_step(self.h, self.pas*(i+1),self.rate,self.pas,self.algo)
        
        tips = self.tangle.get_all_tips()
        tangle1, tangle2 = Tangle.split(self.tangle,self.users[0:int(len(self.users)*self.coef_div)],self.users[int(len(self.users)*self.coef_div):])

        self.rate *= self.coef_div 
        for i in range(int(self.partition_time/self.pas),int(join_time/self.pas)):
            tangle1.simulate_one_step(self.h, self.pas*(i+1),self.rate,self.pas,self.algo,1)
        
        tangle2.set_all_tips(tips)
        self.rate = self.rate/self.coef_div*(1-self.coef_div)
        for i in range(int(self.partition_time/self.pas),int(join_time/self.pas)):    
            tangle2.simulate_one_step(self.h, self.pas*(i+1),self.rate,self.pas,self.algo,-1)
        
        self.tangle = Tangle.join(tangle1,tangle2)

        for i in range(int(join_time/self.pas),number_of_step):
            self.tangle.simulate_one_step(self.h, self.pas*(i+1),self.rate,self.pas,self.algo)
            
        self.tangle.display()
        
        