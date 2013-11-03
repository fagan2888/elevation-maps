import json, urllib2
import datetime

# # options
output = "json"

# definted at https://developers.google.com/maps/documentation/directions/
parameters = "origin=crown+heights,bk,ny"
parameters = parameters + "&destination=manhattan,ny"
parameters = parameters + "&sensor=false"
# parameters = parameters + "&avoid=highways"
# parameters = parameters + "&mode=bicycling"
# parameters = parameters + "&alternatives=true"
query = ("http://maps.googleapis.com/maps/api/directions/%s?%s") % (output, parameters)

# # Obtain data
request = urllib2.urlopen(query)
html = request.read()

data = json.loads(html)

# # Route process
routes = 
