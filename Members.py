from routeTools import Route
from routeTools import Tour
import random

class Member(object):
    def __init__(self, fields, scouts, id):
        self.id = id
        self.fields = fields
        self.scouts = scouts
        self.routeBreak = []
        self.numScouts = len(self.scouts)
        self.routes = [Route(s) for s in self.scouts ]
        self.remaining = []
        self.cost = None
        self.rank = None
        
    def initializeMember(self):
        '''Create random initial solutions'''
        random.shuffle(self.fields)
        self.routeBreak = self.createBreaks(len(self.fields))
        self.assignRoutes(self.fields, self.routeBreak)
        
    def createBreaks(self, total):
        '''Set break points for scouts'''
        routeBreak = []
        for i in range(self.numScouts-1):
            route = random.randint(0, total)
            routeBreak.append(route)
            total = total - route
        routeBreak.append(total)  
        random.shuffle(routeBreak)
        return routeBreak
    
    def assignRoutes(self, fields, routeBreak):
        '''Assign routes using breakpoints'''
        start = 0
        for i, stop in enumerate(routeBreak):
            route = self.routes[i]
            addfields = fields[start:start+stop]
            for field in addfields:
                route.addField(field)
            start += stop
        self.setCost()

    def solution(self):
        return Tour(self.routes)
        
    def setCost(self):
        '''Store cost for member'''
        self.cost = Tour(self.routes).cost()
    
    def twoOpt(self):
        for route in self.routes:
            for i in range(len(route.fields)-2):
                k = i + 1
                while k < len(route.fields):
                    newRoute = Route(route.scout)
                    for field in self.twoOptSwap(route.fields, i, k):
                        newRoute.addField(field)
                    print route    
                    print newRoute
                    if newRoute.cost() < route.cost():
                        route = newRoute
                    k += 1
                
    
    def twoOptSwap(self, route, i, k):
        start = route[0:i-1]
        middle = route[i:k]
        middle = middle[::-1]
        end = route[k+1:]
        newRoute = start + middle + end
        return newRoute

    def mutate(self):
        '''Randomly select two fields and swap their location per route'''
        route = random.choice(self.routes)
        while len(route.fields) < 2:
            route = random.choice(self.routes)
            
        total = len(route.fields)-1            
        index1 = random.randint(0, total)
        index2 = random.randint(0, total)
        while index1 == index2:
            index2 = random.randint(0, total)
        first = route.fields[index1]
        second = route.fields[index2]
        route.fields[index1] = second
        route.fields[index2] = first
        

    
    def __str__(self):
        self.solution()
