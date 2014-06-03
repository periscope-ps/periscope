/*
 * Rest Services for a Node
 * public/js/services/
 * NodeService.js
 */

angular.module('NodeService', []).service('Node', function($http) {

  this.getNodes = function(nodes) {
    $http.get('/api/nodes')
      .success(function(data) {
        console.log('Request: ' + data);
        nodes(data);
      })
      .error(function(data) {
        console.log('Error: ' + data);
      });
  };

});
