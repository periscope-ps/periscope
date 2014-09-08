/*
 * Node Page Controller
 * public/js/controllers/
 * NodeCtrl.js
 */

angular.module('NodeCtrl', []).controller('NodeController', function($scope, Node, Socket) {

  // GET request for initial set of data
  Node.getNodes(function(nodes) {
    $scope.nodes = nodes;
  });

  // New nodes will enter scope through socket
  Socket.on('node_data', function (data) {
    var obj = JSON.parse(data);
    $scope.nodes.push(obj);
  });

});
