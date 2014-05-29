/*
 * Measurement Page Controller
 * public/js/controllers/
 * MeasurementCtrl.js
 */

angular.module('MeasurementCtrl', []).controller('MeasurementController', function($scope, $http) {

  $http.get('/api/measurements')
    .success(function(data) {
      var measurements = data;
      $scope.measurements = measurements;

      console.log(data);
    })
    .error(function(data) {
      console.log('Error: ' + data);
    });

});
