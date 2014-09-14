/*
 * Rest Services for a Measurement
 * public/js/services/
 * MeasurementService.js
 */

angular.module('MeasurementService', []).service('Measurement', function($http, $routeParams, Socket) {
  Socket.emit("measurement_request",{});

  this.getMeasurements = function(measurements) {
    $http.get('/api/measurements/').success(function(data) {
      console.log('Measurement Request: ' + data);
      measurements(data);

      Socket.on('measurement_data',function(data){
        console.log('Measurement Service Request: ' , data);
        measurements(data);
      });
    }).error(function(data) {
      console.log('Measurement Error: ' + data);
    });
  };

  this.getMeasurement = function(measurement) {
    $http.get('/api/measurements/' + $routeParams.id)
      .success(function(data) {
        console.log('Measurement Request: ' + data);
        measurement(data);
      })
      .error(function(data) {
        console.log('Measurement Error: ' + data);
      });
  };
});
