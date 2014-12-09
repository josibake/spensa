import csv



class Manager(object):
    def __init__(self, fileName):
        self.fileName = fileName
        self.distances = {}
        self.fields = []
        lines = self.loadCSV()
        for line in lines:
            self.addDistance(line)
        self.initializeFields()
        
    def loadCSV(self):
        with open(self.fileName, 'rU') as work_file:
            distances = [tuple(map(int, line)) for line in csv.reader(work_file)]
        return distances
    
    def initializeFields(self):
        fieldIDsAlreadyCreated = set()
        for distance in self.distances:
            if distance[0] not in fieldIDsAlreadyCreated:
                if distance[0] == 0:
                    fieldIDsAlreadyCreated.add( distance[0] )
                else:
                    fieldIDsAlreadyCreated.add( distance[0] ) 
                    self.fields.append( Field(distance[0]) )
                
            if distance[1] not in fieldIDsAlreadyCreated:
                if distance[1] == 0:
                    fieldIDsAlreadyCreated.add( distance[1] )
                else:
                    self.fields.append( Field(distance[1]) )
                    fieldIDsAlreadyCreated.add( distance[1] )
    
    def getFields(self):
        return self.fields
    
    def addDistance(self, distance):
        routeLength = distance[3]
        key = (distance[0], distance[1])
        self.distances[key] = routeLength
        otherKey = (distance[1], distance[0])
        self.distances[otherKey] = routeLength

    def distance(self, field1, field2):
        key = (field1, field2)
        routeLength = self.distances[key]
        return routeLength

class Field(object):
    def __init__(self, id):
        self.id = id
    def __str__(self):
        return 'Field %d'%self.id
        
distanceManager = Manager('locations.csv')