from Members import Member
from routeTools import Scout
from FieldManager import distanceManager
from GA import GeneticAlgorithm

'''RECORD: 467 with 5 scouts'''


def main():   
    tsp = TSP(5, 50)
    ga = GeneticAlgorithm(tsp.population)
    for i in range(100000):
        ga.generation(0.01)

    
    print ga.best.solution()

    
    
class TSP(object):
    def __init__(self, numScouts, init):
        self.init = init
        self.fields = distanceManager.getFields()
        self.population = []
        self.scouts = [Scout(i, 10.00 , 0) for i in range(numScouts)]
        self.initializeMembers()
    
    def initializeMembers(self):
        for i in range(self.init):
            member = Member(self.fields, self.scouts, i)
            member.initializeMember()
            self.population.append(member)
        
if __name__ == '__main__':
    main()
    
