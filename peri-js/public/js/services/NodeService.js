/*
 * Rest Services for a Node
 * public/js/services/
 * NodeService.js
 */

angular.module('NodeService', []).service('Node', function($http , Socket) {

  this.getNodes = function(nodes) {
	  $http.get('/api/nodes').success(function(data) {
    	console.log('HTTP Node Request: ' , data);
    	nodes(data);

	  	Socket.on('node_data',function(data){
	  		console.log('Incoming Socket Node Data: ' , data);
	  		nodes(data);
	  	});
    }).error(function(data) {
      console.log('HTTP Node Error: ' , data);
    });
  };
});
