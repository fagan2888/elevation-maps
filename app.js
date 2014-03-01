var http = require('http'),
    express = require('express'),
    app = express();

app.get('/', function(req, res) {
    var origin = '200+E+66th+St.,+NY+NY',
        destination = '36+W+15th+St.,+NY+NY',
        mode = 'bicycling';

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

    var req = http.request(opts, function(request, response) {
        var data = '';
        request.on('data', function(d) {
            data += d;
        });

        request.on('end', function() {
            res.send(JSON.parse(data));
        });
    });

    req.end();
});
app.listen(8000); 
