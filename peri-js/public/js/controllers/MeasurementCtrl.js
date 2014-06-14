/*
 * Measurement Page Controller
 * public/js/controllers/
 * MeasurementCtrl.js
 */

angular.module('MeasurementCtrl', []).controller('MeasurementController', function($scope, $routeParams, $location, Measurement) {

  Measurement.getMeasurements(function(measurements) {
    $scope.measurements = measurements;
  });

  if ($routeParams.id) {
    Measurement.getMeasurement(function(measurement) {
      $scope.measDetails = measurement;
      $scope.measEventTypes = measurement.eventTypes;
      $scope.measConfig = measurement.configuration;
    });
  }

  $scope.showDetails = function(id) {
    $location.path('/measurements/' + id);
  };

});
