/*
 * Rest Services for a Measurement
 * public/js/services/
 * MeasurementService.js
 */

angular.module('MeasurementService', []).service('Measurement', function($http) {

  this.getMeasurements = function(measurements) {
    $http.get('/api/measurements')
      .success(function(data) {
        console.log('Request: ' + data);
        measurements(data);
      })
      .error(function(data) {
        console.log('Error: ' + data);
      });
  };

});
