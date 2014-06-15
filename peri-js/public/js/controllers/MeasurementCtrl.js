/*
 * Measurement Page Controller
 * public/js/controllers/
 * MeasurementCtrl.js
 */

angular.module('MeasurementCtrl', []).controller('MeasurementController', function($scope, $routeParams, $location, Measurement, Service) {

  Measurement.getMeasurements(function(measurements) {
    $scope.measurements = measurements;
  });

  Service.getServices(function(services) {
    $scope.services = services;
  });

  if ($routeParams.id) {
    Measurement.getMeasurement(function(measurement) {
      $scope.measDetails = measurement;
      $scope.measEventTypes = measurement.eventTypes;
      $scope.measConfig = measurement.configuration;
    });
  }

  $scope.getMeasurementService = function(href) {
    var service_id = href.split('/')[4];

    for(var i = 0; $scope.services.length; i++) {
      if ($scope.services[i].id == service_id) {
        return $scope.services[i].name;
      }
    }
  };

  $scope.showDetails = function(id) {
    $location.path('/measurements/' + id);
  };

});
