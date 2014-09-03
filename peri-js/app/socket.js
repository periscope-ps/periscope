/*
 *
 * app/
 * .js
 */

// export function for listening to the socket
module.exports = function (socket) {

  console.log('client connected');

  socket.on('disconnect', function() {
    console.log('client disconnected')
  });

};
