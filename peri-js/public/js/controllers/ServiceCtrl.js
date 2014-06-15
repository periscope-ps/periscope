/*
 * Service Page Controller
 * public/js/controllers/
 * ServiceCtrl.js
 */

angular.module('ServiceCtrl', []).controller('ServiceController', function($scope, Service, Node) {

  Service.getServices(function(services) {
    $scope.services = services;
  });

  Node.getNodes(function(nodes) {
    $scope.nodes = nodes;
  });

  $scope.getServiceNode = function(href) {
    var node_id = href.split('/')[4];

    for(var i = 0; $scope.nodes.length; i++) {
      if ($scope.nodes[i].id == node_id) {
        $scope.node_id = $scope.nodes[i].id;
        return $scope.nodes[i].name;
      }
    }
  };


});
