# all units in meters
from FieldManager import distanceManager as dm
mileageCost = 0.54
pricePerGal = 3.00
mpg = 40233.6

class Scout(object):
    def __init__(self, id, wage = 0, branch = 0):
        self.id = id
        self.wage = wage
        self.branch = branch
    def __str__(self):
        return 'Scout %d'%self.id

class Route(object):
    ''' One scout's trip - sequence of visits '''
    def __init__(self, scout):
        self.scout = scout
        self.fields = []
    
    def addField(self, field):
        self.fields.append(field)

    def cost(self):
        totalCost = self.costFuel() + self.costHourly() + self.costMileage()
        return totalCost
    
    def costFuel(self):
        mileage = self.mileage()
        gallons = float(mileage)/mpg
        return gallons*pricePerGal
        
    def costHourly(self):
        return float(self.scout.wage)*8
        
    def mileage(self):
        if self.fields == []:
            totalCost = 0
            return totalCost
        branch = self.scout.branch
        startLoc = dm.distance(branch,self.fields[0].id)
        endLoc = dm.distance(self.fields[-1].id, branch)
        routeCost = sum(dm.distance(self.fields[i].id, self.fields[i+1].id) for i in range(len(self.fields)-1))
        totalCost = startLoc + routeCost + endLoc
        return totalCost
    
    def costMileage(self):
        return (float(self.mileage())/1609.34)*mileageCost
        
    def __str__(self):
        routeIndexes = [f.id for f in self.fields]
        return 'Route for %s: %s : cost=%d'%(str(self.scout), str(routeIndexes), self.cost())
    
class Tour(object):
    ''' Collection of trips for all of the scouts '''
    def __init__(self, routes):
        self.routes = routes
    
    def cost(self):
        return sum( [r.cost() for r in self.routes] )

    def __str__(self):
        return 'Tour: dist=%d \n%s'%(self.cost(), '\n'.join(map(str, self.routes)))