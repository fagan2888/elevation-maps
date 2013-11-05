# m henry linder, 11/3/13
# run api request to google maps
import json, urllib2
import numpy as np
import datetime

def elevation_increase(locations, output, sensor):
    # submit elevation api request
    query = "http://maps.googleapis.com/maps/api/elevation/%s?"
    query = query + "locations="
    print locations
    for location in locations:
        lat = location['lat']
        lon = location['lng']
        print location
        if query[-1] != "=":
            query = query + "|"
        query = "%f,%f" % (lat, lon)
    query = "&sensor=%s" % (output, start['lat'], start['lng'], end['lat'], end['lng'], sensor)
    request = urllib2.urlopen(query)
    html = request.read()
    data = json.loads(html)
    increase = 0
    results = data['results']
    # iterate forward, effectively making sequential pairs
    results = zip(*[iter(results)]*2)
    for result in results:
        start_elev = result[0]['elevation']
        end_elev = result[1]['elevation']
        
    return end_elev - start_elev


# main loop: loop through different transportation types
proposals = {}
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
        proposals[method][rsumm] = []
        legs = route['legs'] # generally, there will only be one leg
        for leg in legs:
            steps = leg['steps']
            # print leg['distance']['text']
            for step in steps:
                step_loc = []
                step_loc.append(step['start_location'])
                step_loc.append(step['end_location'])
                proposals[method][rsumm].append(step_loc)
