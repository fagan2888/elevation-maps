var exec = require('child_process').exec;

function start(response) {
    console.log("Request handler 'start' was called.");
    var content = 'empty';
    exec('sleep 10', function(err, stdout, stderr) {
        console.log('Finished \'start\'');
        response.writeHead(200, {'Content-Type': 'text/plain'});
        response.write('Ahh, well-rested.');
        response.end();
    });
};

function upload(response) {
    console.log("Request handler 'upload' was called.");
    response.writeHead(200, {'Content-Type': 'text/plain'});
    response.write('Hello upload');
    response.end();
};

exports.start = start;
exports.upload = upload;
