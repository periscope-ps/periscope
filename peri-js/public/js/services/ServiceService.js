/*
 * Rest Services for a Service
 * public/js/services/
 * ServiceService.js
 */

angular.module('ServiceService', []).service('Service', function($http, Socket) {

  this.getServices = function(services) {
    $http.get('/api/services').success(function(data) {
      console.log('HTTP Service Request: ' , data);
      services(data);

      Socket.on('service_data',function(data){
        console.log('Incoming Socket Service Data: ' , data);
        services(data);
      });
    }).error(function(data) {
      console.log('HTTP Service Error: ' ,  data);
    });
  };
});
