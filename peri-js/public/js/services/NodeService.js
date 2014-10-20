/*
 * Rest Services for a Node
 * public/js/services/
 * NodeService.js
 */

angular.module('NodeService', []).service('Node', function($http) {
  // Socket.emit("node_request",{});

  this.getNodes = function(nodes) {
	  $http.get('/api/nodes').success(function(data) {
    	console.log('HTTP Node Request: ' , data);

      var unique_ids = [];
      var unique_nodes = [];

      for(var i = 0; i < data.length; i++) {
        if(unique_ids.indexOf(data[i].id) == -1) {
          unique_ids.push(data[i].id);
          unique_nodes.push(data[i]);
        }
      }

    	nodes(unique_nodes);

	  	/*Socket.on('node_data',function(data){
	  		console.log('Incoming Socket Node Data: ' , data);
	  		nodes(data);
	  	});*/
    }).error(function(data) {
      console.log('HTTP Node Error: ' , data);
    });
  };
});
