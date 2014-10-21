/*
 * Client & UNIS Sockets
 * app/
 * sockets.js
 */

// modules
var WebSocket = require('ws') , freegeoip = require('node-freegeoip');

// export function for listening to the socket
module.exports = function (client_socket,routeMethods) {
  var unis_sub = 'ws://monitor.incntre.iu.edu:9000/subscribe/';
  var ms_sub = 'ws://monitor.incntre.iu.edu:9001/subscribe/';
  var sockets = [];

  // establish client socket
  console.log('Client connected');

  client_socket.on('disconnect', function() {
    console.log('Client disconnected');
  });

  client_socket.on('node_request', function(data) {
    // Create socket to listen for updates on nodes
    var nodeSocket = new WebSocket(unis_sub + 'node');

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
    var serviceSocket = new WebSocket(unis_sub + 'service');

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
    var measurementSocket = new WebSocket(unis_sub + 'measurement');

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
    var metadataSocket = new WebSocket(unis_sub + 'metadata');

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

  client_socket.on('port_request', function(data) {
    // Create socket to listen for updates on port
    var portSocket = new WebSocket(unis_sub + 'port');

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

  client_socket.on('data_id_request', function(data) {
    console.log('UNIS: Data ID requested: ' + data.id);

    for(var i = 0; i < sockets.length; i++) {
      dataSocket = sockets[i];
      dataSocket.close();
    }

    // Create socket to listen for updates on data
    var dataSocket = new WebSocket(ms_sub + 'data/' + data.id);

    sockets.push(dataSocket);

    dataSocket.on('open', function(event) {
      console.log('UNIS: Data ID socket opened for: ' + data.id);
    });

    dataSocket.on('message', function(data) {
      console.log('UNIS: data_id_data: ' + data);
      client_socket.emit('data_id_data', data);
    });

    dataSocket.on('close', function(event) {
      console.log('UNIS: Data ID socket closed for: ' + data.id);
    });
  });

  client_socket.on('data_request', function(data) {
    console.log('UNIS: Data requested: ' + data);

    // Create socket to listen for updates on data
    var dataSocket = new WebSocket(ms_sub + 'data');

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

  client_socket.on('idms_map', function(data) {
	  console.log(data);
	  var ipLs = data.ipArr || [];
	 getAllIpLocationMap(ipLs , function(map){
		client_socket.emit('idms_mapData', {data: map , error : false});
	 });
  });
};


var _nodeLocationMap = {};
function getAllIpLocationMap(array , cb){
	var locMap = {};
	var i =0;
	function done(){
		i++;
		if(i >= array.length - 1){
			cb(locMap);
			// Kil it
			i = -111111;
		}
	}
	array.forEach(function(val) {
		if(_nodeLocationMap[val]){
			locMap[val] = _nodeLocationMap[val];
			done();
		} else
		freegeoip.getLocation(val, function(err, obj) {
			if(err){
				done();
				return ;
			}
			locMap[val] = _nodeLocationMap[val] = [obj.longitude , obj.latitude];
			done();
		});
	});

}

