var exec = require('child_process').exec,
    http = require('http');

function direct(response) {
    console.log("Request handler 'direct' was called.");

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
            dists(data, points, response);
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
                    points.push(step.start_location);
                };
                points.push(step.end_location);

                response.writeHead(200, {'Content-Type': 'text/plain'});
                response.write(String(points));
                response.end();
            };
        };
    };
};

exports.direct = direct;
