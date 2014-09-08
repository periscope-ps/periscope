/*
 * Client & UNIS Sockets
 * app/
 * sockets.js
 */

// modules
var WebSocket = require('ws');

// export function for listening to the socket
module.exports = function (client_socket) {

  // establish client socket
  console.log('Client connected');

  client_socket.on('disconnect', function() {
    console.log('Client disconnected');
  });

  // Create socket to listen for updates on nodes
  var nodeSocket = new WebSocket('ws://localhost:8888/subscribe/node');

  nodeSocket.on('open', function(event) {
    console.log('UNIS: Node socket opened');
  });

  nodeSocket.on('message', function(data) {
    console.log('UNIS: node_data: ' + data);
    client_socket.emit('node_data', data);
  });

  nodeSocket.on('close', function(event) {
    console.log('UNIS: Node socket closed');
  });

};
