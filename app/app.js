var express = require('express'),
    app = express(),
    http = require('http');

app.listen(8000);

app.get('/getopts', function (req, res) {
    // parameters for directions
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

    var req = http.request(opts, function(res) {
        res.setEncoding('utf8');

        var data = '';
        res.on('data', function(d) {
            data += d;
        });

        res.on('end', function() {
            var points = [],
                distances = [];

            data = JSON.parse(data);
            dists(data, points, distances);

            console.log(String(points.length));
            console.log(String(distances));
        });
    });

    req.end();
    res.send();
});

function dists(data, points, distances) {
    rs = data.routes;

    for (var i = 0; i < rs.length; i++) {
        var route = rs[i],
            rtePoints = [],
            distance = 0;
        for (var j = 0; j < route.legs.length; j++) {

            var leg = route.legs[j];
            distance += leg.distance.value;

            var step;
            for (var k = 0; k < leg.steps.length; k++) {
                step = leg.steps[k];
                rtePoints.push(step.start_location);
            };
            rtePoints.push(step.end_location);
        };
        points.push(rtePoints);
        distances.push(distance);
    };
};
