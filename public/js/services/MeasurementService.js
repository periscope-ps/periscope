/*
 * Rest Services for a Node
 * public/js/services/
 * NodeService.js
 */

angular.module('MeasurementService', []).factory('Measurement', ['$http', function($http) {

  return {

    get : function() {
      return $http.get('/api/measurements');
    }//,

    /*create : function(nodeData) {
      return $http.post('/nodes', nodeData);
    },*/

    /*delete : function(id) {
      return $http.delete('/nodes/' + id);
    }*/

  }

}]);
