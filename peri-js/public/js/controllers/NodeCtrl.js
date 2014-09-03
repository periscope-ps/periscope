/*
 * Node Page Controller
 * public/js/controllers/
 * NodeCtrl.js
 */

angular.module('NodeCtrl', []).controller('NodeController', function($scope, Node, Socket) {

  Node.getNodes(function(nodes) {
    $scope.nodes = nodes;
  });

  Socket.emit('cs_emit', 'hello node');

  Socket.on('ss_emit', function (data) {
    $scope.hello_socket = data;
  });

  /*Socket.on('node_data', function (data) {
    $scope.node_data = data;
  });*/

});
