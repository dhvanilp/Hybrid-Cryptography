var http = require('http').createServer().listen(4000);
var io = require('socket.io')(http);
var XMLHttpRequest = require('xmlhttprequest').XMLHttpRequest;

// creating an instance of XMLHttpRequest
var xhttp = new XMLHttpRequest();

// host of the server
var host = 'localhost';
var port = '8000';

console.log('Listening');

// when a connection happens (client enters on the website)
io.on('connection', function(socket) {
    // if the event with the name 'message' comes from the client with the argument 'msgObject',
    // which is an object with the format: {'user_name': < name >, 'message': < message >},
    // it emits for every connected client that a message has been sent, sending the message to the event
    // 'getMessage' in the client side
    socket.on('receive', function(msgObject) {
        // emits the msgObject to the client
        io.emit('getReceive', msgObject);
        console.log(msgObject)
        // url of the view that will process
        var url = 'http://127.0.0.1:8000//';

        // when the request finishes


        // prepares to send
        xhttp.open('POST', url, true);
        // sends the data to the view
        xhttp.send(JSON.stringify(msgObject));
    });

    socket.on('send', function(msgObject) {
        // emits the msgObject to the client
        io.emit('getSend', msgObject);

        // url of the view that will process
        var url = 'http://127.0.0.1:8000//';

        // when the request finishes


        // prepares to send
        xhttp.open('POST', url, true);
        // sends the data to the view
        xhttp.send(JSON.stringify(msgObject));
    });


});