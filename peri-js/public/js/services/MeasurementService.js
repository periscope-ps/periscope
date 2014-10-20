/*
 * Rest Services for a Measurement
 * public/js/services/
 * MeasurementService.js
 */

angular.module('MeasurementService', []).service('Measurement', function($http, $routeParams, Socket) {

  this.getMeasurements = function(measurements) {
    $http.get('/api/measurements/').success(function(data) {
      console.log('HTTP Measurement Request: ' + data);
      measurements(data);

      Socket.on('measurement_data',function(data){
        console.log('Incoming Socket Measurement Data: ' , data);
        measurements(data);
      });
    }).error(function(data) {
      console.log('HTTP Measurement Error: ' + data);
    });
  };

  this.getMeasurement = function(id, measurement) {
    $http.get('/api/measurements/' + id)
      .success(function(data) {
        console.log('HTTP Measurement Request: ' + data);
        measurement(data);
      })
      .error(function(data) {
        console.log('HTTP Measurement Error: ' + data);
      });
  };
});
