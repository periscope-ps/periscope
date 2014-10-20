/*
 * Client & UNIS Sockets
 * app/
 * sockets.js
 */

// modules
var WebSocket = require('ws')
, fs = require('fs');

// export function for listening to the socket
module.exports = function (client_socket) {

  var unis_sub = 'wss://unis.incntre.iu.edu:8443/subscribe/';
  var filePath = '/usr/local/etc/node.info';

  fs.readFile(filePath, {encoding: 'utf-8'}, function(err, data) {
    var ms_host = '';
    var ms_port = '';

    if (err) {
      console.log('file read error: ' + err);
    } else {
      var fileData = data.toString().split('\n');

      for(line in fileData) {
        split = fileData[line].split('=');

        if(split[0] === 'ms_instance') {
          ms_url = split[1];
          ms_port = ms_url.split(":")[2];
          ms_host = ms_url.split("//")[1].split(":")[0];
      }
    }
   }
  });

  var ms_sub = 'wss://' + ms_host + ':' + ms_port + '/subscribe/';

  var ssl_opts = {'cert': fs.readFileSync('/usr/local/etc/certs/unis-proxy.pem'),
                  'key': fs.readFileSync('/usr/local/etc/certs/unis-proxy.pem'),
                  rejectUnauthorized: false};

  console.log('UNIS subscribe: ' + unis_sub);
  console.log('MS subscribe: ' + ms_sub);

  // establish client socket
  console.log('Client connected');

  client_socket.on('disconnect', function() {
    console.log('Client disconnected');
  });

  client_socket.on('node_request', function(data) {
    // Create socket to listen for updates on nodes
    var nodeSocket = new WebSocket(unis_sub + 'node', ssl_opts);

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
  });

  client_socket.on('service_request', function(data) {
    // Create socket to listen for updates on services
    var serviceSocket = new WebSocket(unis_sub + 'service', ssl_opts);

    serviceSocket.on('open', function(event) {
      console.log('UNIS: Service socket opened');
    });

    serviceSocket.on('message', function(data) {
      console.log('UNIS: service_data: ' + data);
      client_socket.emit('service_data', data);
    });

    serviceSocket.on('close', function(event) {
      console.log('UNIS: Service socket closed');
    });
  });

  client_socket.on('measurement_request', function(data) {
    // Create socket to listen for updates on measurements
    var measurementSocket = new WebSocket(unis_sub + 'measurement', ssl_opts);

    measurementSocket.on('open', function(event) {
      console.log('UNIS: Measurement socket opened');
    });

    measurementSocket.on('message', function(data) {
      console.log('UNIS: measurement_data: ' + data);
      client_socket.emit('measurement_data', data);
    });

    measurementSocket.on('close', function(event) {
      console.log('UNIS: Measurement socket closed');
    });
  });

  client_socket.on('metadata_request', function(data) {
    // Create socket to listen for updates on metadata
    var metadataSocket = new WebSocket(unis_sub + 'metadata', ssl_opts);

    metadataSocket.on('open', function(event) {
      console.log('UNIS: Metadata socket opened');
    });

    metadataSocket.on('message', function(data) {
      console.log('UNIS: metadata_data: ' + data);
      client_socket.emit('metadata_data', data);
    });

    metadataSocket.on('close', function(event) {
      console.log('UNIS: Metadata socket closed');
    });
  });

  client_socket.on('data_id_request', function(data) {
    console.log('UNIS: Data ID requested: ' + data.id);
    console.log(ms_sub+'data/'+data.id);

    // Create socket to listen for updates on data
    var dataSocket = new WebSocket(ms_sub + 'data/' + data.id, ssl_opts);

    dataSocket.on('open', function(event) {
      console.log('UNIS: Data ID socket opened');
    });

    dataSocket.on('message', function(data) {
      console.log('UNIS: data_id_data: ' + data);
      client_socket.emit('data_id_data', data);
    });

    dataSocket.on('close', function(event) {
      console.log('UNIS: Data ID socket closed');
    });
  });

  client_socket.on('data_request', function(data) {
    console.log('UNIS: Data requested: ' + data);

    // Create socket to listen for updates on data
    var dataSocket = new WebSocket(ms_sub + 'data', ssl_opts);

    dataSocket.on('open', function(event) {
      console.log('UNIS: Data socket opened');
    });

    dataSocket.on('message', function(data) {
      console.log('UNIS: data_data: ' + data);
      client_socket.emit('data_data', data);
    });

    dataSocket.on('close', function(event) {
      console.log('UNIS: Data socket closed');
    });
  });

  client_socket.on('port_request', function(data) {
    // Create socket to listen for updates on port
    var portSocket = new WebSocket(unis_sub + 'port', ssl_opts);

    portSocket.on('open', function(event) {
      console.log('UNIS: Port socket opened');
    });

    portSocket.on('message', function(data) {
      console.log('UNIS: port_data: ' + data);
      client_socket.emit('port_data', data);
    });

    portSocket.on('close', function(event) {
      console.log('UNIS: Port socket closed');
    });
  });
};
