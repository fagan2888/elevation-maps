import json, urllib2
import datetime

# # options
host='http://maps.googleapis.com/maps/api/directions/'
key = 'AIzaSyBiAuec2f8kYqcfRUEHfgkMcgdUUhDkgXM'
output = 'json'

sensor = 'false'
query = 'origin=brooklyn&destination=manhattan'
query = query + sensor
query = query + '&avoid=highways'
query = query + '&mode=bicycling'


# # Obtain data
query = '/'.join( [host, key] + (output + '?') + )
# request = urllib2.urlopen(query)
# html = request.read()

# data = json.loads(html)
