# m henry linder, 11/3/13
# run api request to google maps
import json, urllib2
import datetime

def elevation_change(start, end, output, sensor):
    # submit elevation api request
    query = "http://maps.googleapis.com/maps/api/elevation/%s?locations=%f,%f|%f,%f&sensor=%s" % (output, start['lat'], start['lng'], end['lat'], end['lng'], sensor)
    request = urllib2.urlopen(query)
    html = request.read()
    data = json.loads(html)

# # options
output = "json"

sensor = "false"

# definted at https://developers.google.com/maps/documentation/directions/
parameters = "origin=columbus+circle,ny"
parameters = parameters + "&destination=union+square,ny"
parameters = parameters + "&sensor=%s" % sensor
parameters = parameters + "&avoid=highways"
parameters = parameters + "&mode=bicycling" # setting to walking reduces number of alternatives
parameters = parameters + "&alternatives=true"
query = ("http://maps.googleapis.com/maps/api/directions/%s?%s") % (output, parameters)

# # Obtain data
request = urllib2.urlopen(query)
html = request.read()

data = json.loads(html)

# # Route process
routes = data['routes']
for route in routes:
    print route['summary']
    legs = route['legs']
    for leg in legs:
        steps = leg['steps']
        for step in steps:
            print step['start_location'], step['end_location']
    print
