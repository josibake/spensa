from routeTools import Route
from routeTools import Tour
from Members import Member
import random

class GeneticAlgorithm(object):
    def __init__(self, population):
        self.population = population
        self.population.append(Dummy())
        self.rank()
        self.best = None
        
    def generation(self, p):
        children = []
        self.rank()
        mIndex = self.spinWheel()
        fIndex = self.spinWheel()
        child1 = self.crossover(self.population[mIndex], self.population[fIndex])
        if random.random() < p:
            child1.mutate()
        if child1.cost < self.population[mIndex].cost:
            self.population[mIndex] = child1            
        child2 = self.crossover(self.population[fIndex],self.population[mIndex])
        if random.random() < p:
            child2.mutate()
        if child2.cost < self.population[fIndex].cost:
            self.population[fIndex] = child2
        
    def spinWheel(self):
        '''Selects member for breeding using Ranked Roullette Wheel'''
        total = sum(range(len(self.population)))
        selector = random.randint(1,total)
        value = 0
        for index, member in reversed(list(enumerate(self.population))):
            value += index
            if value >= selector:
                return index
                break
    
    def rank(self):
        '''Ranks population based on cost.  Highest rank = lowest cost'''
        self.population.sort(key=lambda x: x.cost, reverse=True)
        self.best = self.population[-1]
        
    
    def crossover(self, mother, father):
        remaining = []
        id = len(self.population)+1
        child = Member(mother.fields, mother.scouts, id)
        for i, route in enumerate(child.routes):
            length = random.randint(0, len(mother.routes[i].fields))
            start = random.randint(0, len(mother.routes[i].fields)-length)
            childSegment = mother.routes[i].fields[start:start+length]
            for field in childSegment:
                route.addField(field)
            for field in (mother.routes[i].fields[:start] + mother.routes[i].fields[start+length:]):
                remaining.append(field)
        fatherGenes = [field for route in father.routes for field in route.fields]
        ordered = [field for field in fatherGenes if field in remaining]
        newBreaks = child.createBreaks(len(ordered))
        child.assignRoutes(ordered, newBreaks)
        return child
    
    

class Dummy(object):
    def __init__(self):
        '''Creates Dummy value as placeholder for zero'''
        self.cost = 'inf'
    def __str__(self):
        return "Dummy"
    
    
