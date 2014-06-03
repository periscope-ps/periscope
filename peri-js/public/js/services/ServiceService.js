/*
 * Rest Services for a Service
 * public/js/services/
 * ServiceService.js
 */

angular.module('ServiceService', []).service('Service', function($http) {

  this.getServices = function(services) {
    $http.get('/api/services')
      .success(function(data) {
        console.log('Request: ' + data);
        services(data);
      })
      .error(function(data) {
        console.log('Error: ' + data);
      });
  };

});
