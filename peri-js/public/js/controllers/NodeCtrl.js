/*
 * Node Page Controller
 * public/js/controllers/
 * NodeCtrl.js
 */

angular.module('NodeCtrl', []).controller('NodeController', function($scope, Node) {

  // GET request for initial set of data
  // Request a socket connection
  // New data will enter scope through socket
  Node.getNodes(function(nodes) {
    $scope.nodes = $scope.nodes || [];

    if (typeof nodes =='string')
    	nodes = JSON.parse(nodes);

    $scope.nodes = $scope.nodes.concat(nodes);
  });
});
