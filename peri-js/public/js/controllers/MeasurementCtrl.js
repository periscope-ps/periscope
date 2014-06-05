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
      alert(measurement.eventTypes);
      $scope.measDetails = measurement;
    });
  }

  $scope.showDetails = function(id) {
    $location.path('/measurements/' + id);
  };

});
