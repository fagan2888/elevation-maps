// references:
// 1. http://chimera.labs.oreilly.com/books/1234000001808/ch02.html#I_sect12_d1e1886
// 2. http://nodejs.org/api/http.html
//
var http = require('http');

var origin = '200+E+66th+St.,+NY+NY',
    destination = '600+Lincoln+Pl.,+Brooklyn+NY',
    mode = 'driving';

var query = '/maps/api/directions';
query += '/json';
query += '?sensor=false';
query += '&avoid=highways';
query += '&alternatives=true';
query += '&origin=' + origin;
query += '&destination=' + destination;
query += '&travelMode=' + mode;

var opts = {
    host: 'maps.googleapis.com',
    path: query,
    port: 80,
    method: 'GET'
};

var routes = [];
var i;
var req = http.request(opts, function(res) {
    res.setEncoding('utf8');

    var data = '';
    res.on('data', function(d) {
        data += d;
    });

    res.on('end', function() {
        data = JSON.parse(data);
        var points = [];
        dists(data, points);
    });
});

req.end();

function dists(data, points) {
    rs = data.routes;
    for (i = 0; i < rs.length; i++) {

        var route = rs[i];
        for (var j = 0; j < route.legs.length; j++) {

            var leg = route.legs[j];
            var step;
            for (var k = 0; k < leg.steps.length; k++) {

                step = leg.steps[k];
                console.log(step);
                points.push(step.start_location);
            };
            points.push(step.end_location);
        };
    };
};
