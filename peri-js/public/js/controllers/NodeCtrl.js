/*
 * Node Page Controller
 * public/js/controllers/
 * NodeCtrl.js
 */

angular.module('NodeCtrl', []).controller('NodeController', function($scope, Node, Socket) {

  // GET request for initial set of data
  Node.getNodes(function(nodes) {
    $scope.nodes = $scope.nodes || [];
    if (typeof nodes =='string')
    	nodes = JSON.parse(nodes);
    $scope.nodes = $scope.nodes.concat(nodes);
  });

  // request a socket connection
 // Socket.emit('node_request', {});

  // New data will enter scope through socket
  /*
  Socket.on('node_data', function (data) {
    var obj = JSON.parse(data);
    $scope.nodes.push(obj);
  });*/

});
