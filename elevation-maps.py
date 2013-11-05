# m henry linder, 11/3/13
# run api request to google maps
import json, urllib2
from pandas import DataFrame
import numpy as np

def elevation_request(locations, output, sensor):
    # submit elevation api request
    query = "http://maps.googleapis.com/maps/api/elevation/%s?" % (output)
    query = query + "&sensor=%s" % sensor
    query = query + "&locations="
    for location in locations.values:
        lat = location[0]
        lon = location[1]
        if query[-1] != "=":
            query = query + "|"
        query = query + "%f,%f" % (lat, lon)
    print query

    request = urllib2.urlopen(query)
    html = request.read()
    data = json.loads(html)
    return data
    # increase = 0
    # results = data['results']
    # # iterate forward, effectively making sequential pairs
    # results = zip(*[iter(results)]*2)
    # for result in results:
        # start_elev = result[0]['elevation']
        # end_elev = result[1]['elevation']
        
    # return end_elev - start_elev


# main loop: loop through different transportation types
proposals = {}
points = []
transit = ['bicycling','walking','driving']
for method in transit:
    proposals[method] = {}
    # # options
    output = "json"
    sensor = "false"

    # start = raw_input('Start location: ')
    # end = raw_input('End location: ')
    start = "200 E 66th St., NY NY"
    end = "36 W 15th St. NY NY"
    start = start.replace(" ", "+")
    end = end.replace(" ", "+")


    # defined at https://developers.google.com/maps/documentation/directions/
    parameters = "origin=%s" % start
    parameters = parameters + "&destination=%s" % end
    parameters = parameters + "&sensor=%s" % sensor
    parameters = parameters + "&avoid=highways"
    parameters = parameters + "&travelMode=%s" % method # setting to walking reduces number of alternatives
    parameters = parameters + "&alternatives=true"
    query = ("http://maps.googleapis.com/maps/api/directions/%s?%s") % (output, parameters)

    # # Obtain data
    request = urllib2.urlopen(query)
    html = request.read()

    data = json.loads(html)

    # # Route process
    routes = data['routes']
    for route in routes: # each possible route
        rsumm = route['summary']
        proposals[method][rsumm] = [] # steps for this route
        legs = route['legs'] # generally, there will only be one leg
        for leg in legs:
            steps = leg['steps']
            for step in steps:
                # record start, end
                step_loc = []
                step_loc.append(step['start_location'])
                step_loc.append(step['end_location'])
                proposals[method][rsumm].append(step_loc)

                # keep each point
                points.append(step['start_location'])
            points.append(step['end_location']) # add last location, tok
points = DataFrame(points)
points.columns = ['lat','lon']

d = elevation_request(points, output, sensor)
