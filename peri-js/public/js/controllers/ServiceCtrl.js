/*
 * Service Page Controller
 * public/js/controllers/
 * ServiceCtrl.js
 */

angular.module('ServiceCtrl', []).controller('ServiceController', function($scope, Service, Node, Socket) {

  Service.getServices(function(services) {
    $scope.services = services;
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

  // request a socket connection
  Socket.emit('service_request', {});

  // New data will enter scope through socket
  Socket.on('service_data', function (data) {
    var obj = JSON.parse(data);
    $scope.services.push(obj);
  });
});
