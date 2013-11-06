# m henry linder, 11/3/13
# run api request to google maps
import json, requests
from pandas import DataFrame, Series
import numpy as np

# request the elevation for multiple locations
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

    request = requests.get(query)
    html = request.text
    data = json.loads(html)
    return data


# # main loop: loop through different transportation types, record routes
proposals = {}
statistics = {}
points = []

transit = ['bicycling','walking','driving']
for method in transit:
    proposals[method] = {}
    statistics[method] = {}
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
    request = requests.get(query)
    html = request.text

    data = json.loads(html)

    # # Route process
    routes = data['routes']
    for route in routes: # each possible route
        rsumm = route['summary']
        proposals[method][rsumm] = [] # steps for this route
        statistics[method][rsumm] = {}

        legs = route['legs'] # generally, there will only be one leg
        for leg in legs:
            steps = leg['steps']
            distance = 0
            for step in steps:
                # record start, end
                step_loc = []
                step_loc.append(step['start_location'])
                step_loc.append(step['end_location'])
                proposals[method][rsumm].append(step_loc)
                
                # update distance travelled
                distance = distance + step['distance']['value']

                # keep each point
                points.append(step['start_location'])
            points.append(step['end_location']) # add last location, too
            
            # record distance travelled
            statistics[method][rsumm]['distance'] = distance

points = DataFrame(points)
points.columns = ['lat','lon']
step_copy = step

# incorporate elevation information into points dataframe
elevations = elevation_request(points, output, sensor)
elevations = elevations['results']
points['elevation'] = Series(index=points.index)
for i in np.arange(len(elevations)):
    points.ix[i]['elevation'] = elevations[i]['elevation']

# loop back over all routes
for mode in proposals.keys():
    for route in proposals[mode].keys():
        numsteps = len(route)
        increase_total = 0
        decrease_total = 0

        for step in proposals[mode][route]:
            start_pt = points[np.all([points['lat']==step[0]['lat'],
                                      points['lon']==step[0]['lng']],0)].iloc[0]
            start_elev = start_pt['elevation']
            end_pt = points[np.all([points['lat']==step[1]['lat'],
                                    points['lon']==step[1]['lng']],0)].iloc[0]
            end_elev = end_pt['elevation']

            # calculate change in elevation for this step
            diff = end_elev - start_elev
            if diff >= 0: # increase in height
                increase_total = increase_total + diff
            else: # decrease in height
                decrease_total = decrease_total + diff
        statistics[mode][route]['numsteps'] = numsteps
        statistics[mode][route]['increase_total'] = increase_total
        statistics[mode][route]['decrease_total'] = decrease_total

