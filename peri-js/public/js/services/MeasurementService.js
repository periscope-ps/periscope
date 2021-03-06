/*
 * Rest Services for a Measurement
 * public/js/services/
 * MeasurementService.js
 */

angular.module('MeasurementService', []).service('Measurement', function($http, $routeParams) {

  this.getMeasurements = function(measurements) {
    $http.get('/api/measurements/')
      .success(function(data) {
        console.log('Measurement Request: ' + data);
        measurements(data);
      })
      .error(function(data) {
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
