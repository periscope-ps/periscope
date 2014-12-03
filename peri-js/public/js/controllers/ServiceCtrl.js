/*
 * Service Page Controller
 * public/js/controllers/
 * ServiceCtrl.js
 */

angular.module('ServiceCtrl', []).controller('ServiceController', function($scope, Service, Node) {
	var start = 0 , pagingSize = 10 ;
	$scope.serviceBusy = false;
	$scope.loadMore = function() {
		$scope.serviceBusy = true;
		Service.getServices(function(services , count ){
			if (typeof services =='string')
			      services = JSON.parse(services);
			$scope.services = $scope.services.concat(services);
			start += services.length ;
			if(start < count && services.length != 0)
				$scope.serviceBusy = false ;
		},start, start + pagingSize);			
	};	
  // GET request for initial set of data
  // Request a socket connection
  // New data will enter scope through socket
  Service.getServices(function(services) {
    $scope.services = $scope.services || [];

    if (typeof services =='string')
      services = JSON.parse(services);

    $scope.services = $scope.services.concat(services);
    start += services.length ;
  });

  Node.getNodes(function(nodes) {
    $scope.nodes = nodes;

    $scope.getServiceNode = function(service) {

      if(service.runningOn != null) {
        var node_id = service.runningOn.href.split('/')[4];
      } else {
        return 'Node Unknown';
      }

      for(var i = 0; i < $scope.nodes.length; i++) {
        if ($scope.nodes[i].id == node_id) {
            return $scope.nodes[i].name;
        } else {
          return 'Node Unknown';
        }
      }
    };
  });

});
