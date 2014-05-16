/*
 * Rest Services for BLiPP
 * public/js/services/
 * BlippService.js
 */

angular.module('BlippService', []).factory('Blipp', ['$http', function($http) {

  return {

    get : function() {
      return $http.get('/nodes');
    }//,

    /*create : function(nodeData) {
      return $http.post('/nodes', nodeData);
    },*/

    /*delete : function(id) {
      return $http.delete('/nodes/' + id);
    }*/

  }

}]);
