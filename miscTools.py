import csv
import json
import urllib

#Loads fields as a dictionary and gives them a unique ID
def load_fields(file_name):
    with open(file_name, 'rU') as fields:
        data = csv.DictReader(fields)
        
        locations = {}
        for line in data:
            key = line['id']
            locations[key] = {
                'name':line['name'],
                'lat':line['lat'],
                'lon':line['lon']
            } 
    
        for i in range(len(locations)):
            for k, v in locations[str(i)].iteritems():
                locations[str(i)][k] = v.strip()
    return locations

#Saves distance_matrix as a CSV - to avoid having to re-query google
def save_csv(results):
    item_length = len(results)
    with open('locations.csv', 'wb') as write_file:
        file_writer = csv.writer(write_file)
        for i in range(item_length):
            file_writer.writerow([x for x in results[i]])
            

#Loads distance_matrix from csv file
def load_csv(file_name):
    with open(file_name, 'rU') as work_file:
        distance_matrix = [tuple(map(int, line)) for line in csv.reader(work_file)]
    return distance_matrix

#Queries google with each pair and returns a distance and time.  Stores pair, time, distance as a tuple
def google_query(distances):
    results = []
    url_dict = {'key':'AIzaSyCOxEv7UoRoYnwCeKoxAIdzXktgy2_QRt8', 'units':'imperial', 'destinations':'lat,lon', 'origins':'lat,lon'}
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
    for pair in distances:
    
        url_dict['origins'] = locations[str(pair[0])]['lat'] + "," + locations[str(pair[0])]['lon']
        url_dict['destinations'] = locations[str(pair[1])]['lat'] + "," + locations[str(pair[1])]['lon']

        query = url+urllib.urlencode(url_dict, True)
    
        result = json.load(urllib.urlopen(query))
        data = (str(pair[0]), str(pair[1]), result['rows'][0]['elements'][0]['duration']['value'], result['rows'][0]['elements'][0]['distance']['value'])
        results.append(data)

    return results