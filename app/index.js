var server = require('./server'),
    router = require('./router'),
    requestHandlers = require('./requestHandlers');

var handle = {};
handle['/'] = requestHandlers.direct;

server.start(router.route, handle);
