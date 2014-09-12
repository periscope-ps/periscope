/*
 * Rest Services for a Node
 * public/js/services/
 * NodeService.js
 */

angular.module('NodeService', []).service('Node', function($http , Socket) {
  Socket.emit("node_request",{});
  this.getNodes = function(nodes) {
	 $http.get('/api/nodes').success(function(data) {
    	console.log('Node Request: ' , data);
    	nodes(data);
	  	Socket.on('node_data',function(data){
	  		console.log('Node Request: ' , data);		
	  		nodes(data);
	  	});
    }).error(function(data) {
      console.log('Node Error: ' + data);
    });
  };
});
