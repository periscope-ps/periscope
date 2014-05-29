/*
 * Rest Services for a Node
 * public/js/services/
 * NodeService.js
 */

angular.module('NodeService', []).factory('Node', ['$http', function($http) {

  return {

    get : function() {
      return $http.get('/api/nodes');
    }//,

    /*create : function(nodeData) {
      return $http.post('/nodes', nodeData);
    },*/

    /*delete : function(id) {
      return $http.delete('/nodes/' + id);
    }*/

  }

}]);
