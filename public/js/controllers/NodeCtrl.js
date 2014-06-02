/*
 * Node Page Controller
 * public/js/controllers/
 * NodeCtrl.js
 */

angular.module('NodeCtrl', []).controller('NodeController', function($scope, Node) {

  Node.getNodes(function(nodes) {
    $scope.nodes = nodes;
  });

});
