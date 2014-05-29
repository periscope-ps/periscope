/*
 * Rest Services for a Service
 * public/js/services/
 * ServiceService.js
 */

angular.module('ServiceService', []).factory('Service', ['$http', function($http) {

  return {

    get : function() {
      return $http.get('/api/services');
    }//,

    /*create : function(serviceData) {
      return $http.post('/services', serviceData);
    },*/

    /*delete : function(id) {
      return $http.delete('/services/' + id);
    }*/

  }

}]);
