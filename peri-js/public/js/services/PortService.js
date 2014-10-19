/*
 * Rest Services for a Port
 * public/js/services/
 * PortService.js
 */

angular.module('PortService', []).service('Port', function($http) {

  this.getPorts = function(ports) {
    $http.get('/api/ports')
      .success(function(data) {
        console.log('HTTP Port Request: ' + data);
        ports(data);
      })
      .error(function(data) {
        console.log('HTTP Port Error: ' + data);
      });
  };

});
