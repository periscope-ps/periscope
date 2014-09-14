/*
 * Measurement Page Controller
 * public/js/controllers/
 * MeasurementCtrl.js
 */

angular.module('MeasurementCtrl', []).controller('MeasurementController', function($scope, $routeParams, $location, Measurement, Metadata, Service, Node) {

  var measurement_id = $routeParams.id;

  Measurement.getMeasurements(function(measurements) {
    $scope.measurements = $scope.measurements || [];

    if (typeof measurements =='string')
      measurements = JSON.parse(measurements);

    $scope.measurements = $scope.measurements.concat(measurements);
  });
  Service.getServices(function(services) {
    $scope.services = $scope.services || [];

    if (typeof services =='string')
      services = JSON.parse(services);

    $scope.services = $scope.services.concat(services);
  });
  Node.getNodes(function(nodes) {
    $scope.nodes = $scope.nodes || [];

    if (typeof nodes =='string')
      nodes = JSON.parse(nodes);

    $scope.nodes = $scope.nodes.concat(nodes);
  });

  if (measurement_id) {
    Measurement.getMeasurement(function(measurement) {
      $scope.measurement = measurement;
    });
    Metadata.getMetadatas(function(metadatas) {
      $scope.metadatas = metadatas;
      var measurementMetadata = [];

      for(var i = 0; i < $scope.metadatas.length; i++) {
        if ($scope.metadatas[i].parameters.measurement.href.split("/")[4] === measurement_id) {
          measurementMetadata.push($scope.metadatas[i]);
        }
      }
      $scope.measurementMetadata = measurementMetadata;
    });
  }

  $scope.getMeasurementService = function(href) {
    var service_id = href.split('/')[4];

    for(var i = 0; i < $scope.services.length; i++) {
      if ($scope.services[i].id == service_id) {
        return $scope.services[i].name;
      }
    }
  };

  $scope.getMeasurementNode = function(href) {
    var node_id = href.split('/')[4];

    for(var i = 0; i < $scope.nodes.length; i++) {
      if ($scope.nodes[i].id == node_id) {
        return $scope.nodes[i].name;
      }
    }
  };

  $scope.measOFF = function() {
    if ($scope.measurement.configuration.status === 'ON') {
      return false;
    } else {
      return true;
    }
  };

  /*$scope.measPUT = function(measurement) {

    if (measurement.$invalid) {
      // If form is invalid, return and let AngularJS show validation errors.
      $scope.addAlert('Invalid form, cannot be submitted', 'danger');
      $scope.alert = true;
      return;
    } else {
      // copy data submitted by form
      $scope.measurementData = angular.copy(measurement);

      $scope.measurementData["status"] = "ON";

      $http({
        method: 'PUT',
        url: '/api/measurements/' + $scope.measurementData.id,
        data: $scope.measurementData,
        headers: {'Content-type': 'application/perfsonar+json', 'Content-Length': $scope.measurementData.length}
      }).
      success(function(data, status, headers, config) {
        $scope.addAlert(data, 'success');
        $scope.addAlert(status, 'success');
        $scope.addAlert(headers, 'success');
        $scope.addAlert(config, 'success');
        $scope.addAlert('Measurement: ' + JSON.stringify(data) + ' has been edited', 'success');
        $scope.alert = true;
      }).
      error(function(data, status, headers, config) {
        $scope.addAlert(data, 'danger');
        $scope.addAlert(status, 'danger');
        $scope.addAlert(headers, 'danger');
        $scope.addAlert(config, 'danger');
        $scope.addAlert('Status: ' + status.toString() + ', ' + 'Error: ' + data.error.message, 'danger');
        $scope.alert = true;
      });
    }
  };*/

  /*$scope.measDELETE = function(measurement) {

    if (measurement.$invalid) {
      // If form is invalid, return and let AngularJS show validation errors.
      $scope.addAlert('Invalid form, cannot be submitted', 'danger');
      $scope.alert = true;
      return;
    } else {
      // copy data submitted by form
      $scope.measurementData = angular.copy(measurement);

      $scope.measurementData["status"] = "OFF";

      $http({
        method: 'DELETE',
        url: '/api/measurements/' + $scope.measurementData.id,
        data: $scope.measurementData,
        headers: {'Content-type': 'application/perfsonar+json', 'Content-Length': $scope.measurementData.length}
      }).
      success(function(data, status, headers, config) {
        $scope.addAlert(data, 'success');
        $scope.addAlert(status, 'success');
        $scope.addAlert(headers, 'success');
        $scope.addAlert(config, 'success');
        $scope.addAlert('Measurement: ' + JSON.stringify(data) + ' turned off', 'success');
        $scope.alert = true;
      }).
      error(function(data, status, headers, config) {
        $scope.addAlert(data, 'danger');
        $scope.addAlert(status, 'danger');
        $scope.addAlert(headers, 'danger');
        $scope.addAlert(config, 'danger');
        $scope.addAlert('Status: ' + status.toString() + ', ' + 'Error: ' + data.error.message, 'danger');
        $scope.alert = true;
      });
    }
  };*/

  $scope.showDetails = function(measurement_id) {
    $location.path('/measurements/' + measurement_id);
  };
  $scope.showMetadataData = function(metadata_id) {
    $location.path('/metadata/' + metadata_id);
  };

});
