/*
 * Client & UNIS Socket API
 * app/
 * sockets.js
 */

// export function for listening to the socket
module.exports = function (client_socket) {

  var socket_server = require('socket.io');

  // establish client socket
  console.log('client connected');

  // client/server socket hello world
  client_socket.on('cs_emit', function(data) {
    console.log('client says, ' + data);
  });

  client_socket.emit('ss_emit', 'hello angular');

  client_socket.on('disconnect', function() {
    console.log('client disconnected');
  });


  // Create socket to listen for updates on nodes
  // todo: handle no socket to connection to case
  /*var nodes_socket = new socket_server('ws://localhost:8888/subscribe/node');

  nodes_socket.on('connection', function(event) {
    console.log('Connected to nodes socket');
  });

  nodes_socket.on('message', function(data) {
    console.log(data);

    // data from our socket will be broadcast to the client
    client_socket.broadcast.emit('node_data', data);
  });

  nodes_socket.on('disconnect', function(event) {
    console.log('Disconnected from nodes socket');
  });*/

};
