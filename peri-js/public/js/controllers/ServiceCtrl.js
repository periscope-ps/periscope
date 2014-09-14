/*
 * Service Page Controller
 * public/js/controllers/
 * ServiceCtrl.js
 */

angular.module('ServiceCtrl', []).controller('ServiceController', function($scope, Service, Node) {

  // GET request for initial set of data
  // Request a socket connection
  // New data will enter scope through socket
  Service.getServices(function(services) {
    $scope.services = $scope.services || [];

    if (typeof services =='string')
      services = JSON.parse(services);

    $scope.services = $scope.services.concat(services);
  });

  Node.getNodes(function(nodes) {
    $scope.nodes = nodes;
  });

  $scope.getServiceNode = function(href) {
    var node_id = href.split('/')[4];

    for(var i = 0; i < $scope.nodes.length; i++) {
      if ($scope.nodes[i].id == node_id) {
          return $scope.nodes[i].name;
      }
    }
  };
});
