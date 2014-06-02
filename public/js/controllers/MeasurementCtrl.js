/*
 * Measurement Page Controller
 * public/js/controllers/
 * MeasurementCtrl.js
 */

angular.module('MeasurementCtrl', []).controller('MeasurementController', function($scope, Measurement) {

  Measurement.getMeasurements(function(measurements) {
    $scope.measurements = measurements;
  });

});
