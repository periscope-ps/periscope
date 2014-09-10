/*
 * Rest Services for a Node
 * public/js/services/
 * NodeService.js
 */

angular.module('NodeService', []).service('Node', function($http , Socket) {
  this.getNodes = function(nodes) {
	Socket.emit("node_request",{blah : 213123123});
	Socket.on('node_data',function(data){
		console.log('received data');
		 var obj = JSON.parse(data);
		 console.log('Node Request: ' , data);		
		 nodes(obj);
	});    
  };
});
