from user import *
from tangle import *
from transaction import parameters

#class
class Simulation:
    def __init__(self):
        self.users = [User(i+1,10) for i in range(parameters["nb users"])]
        self.tangle = Tangle(self.users)

        
    def simulate(self):
        number_of_step = int(parameters["total time"]/parameters['pas'])
        for i in range(number_of_step):
            self.tangle.simulate_one_step(parameters['pas']*(i+1))
        self.tangle.display()
        
        return self.tangle


class SimulationSplit(Simulation):

    def __init__(self):
        Simulation.__init__(self)


    def simulate(self):
        number_of_step=int(parameters['total time']/parameters['pas'])
        for i in range(int(parameters['partition time']/parameters['pas'])):
            self.tangle.simulate_one_step(parameters['pas']*(i+1))

        tangle1, tangle2 = Tangle.split(self.tangle,self.users[0:int(len(self.users)*parameters['coef div'])],self.users[int(len(self.users)*parameters['coef div']):])

        parameters['rate'] *= parameters['coef div']
        for i in range(int(parameters['partition time']/parameters['pas']),int(parameters['join time']/parameters['pas'])):
            tangle1.simulate_one_step(parameters['pas']*(i+1),1)
        

        parameters['rate'] = parameters['rate']/parameters['coef div']*(1-parameters['coef div'])
        for i in range(int(parameters['partition time']/parameters['pas']),int(parameters['join time']/parameters['pas'])):
            tangle2.simulate_one_step(parameters['pas']*(i+1),-1)
        
        self.tangle = Tangle.join(tangle1,tangle2)
        parameters['rate'] = parameters['rate'] / (1 - parameters['coef div'])
        for i in range(int(parameters['join time']/parameters['pas']),number_of_step):
            self.tangle.simulate_one_step(parameters['pas']*(i+1))
            
        self.tangle.display()
        
        