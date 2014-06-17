/*
 * Measurement Page Controller
 * public/js/controllers/
 * MeasurementCtrl.js
 */

angular.module('MeasurementCtrl', []).controller('MeasurementController', function($scope, $http, $routeParams, $location, Measurement, Service) {

  var meas_id = $routeParams.id;

  // $scope.eventData = {};
  $scope.measData = {};
  // $scope.alerts = [];
  $scope.timeTypes = [
        {type:'Seconds'},
        {type:'Minutes'},
        {type:'Hours'},
        {type:'Days'}
  ];

  /*$scope.toggleEdit = function() {
    $scope.btnEdit = $scope.btnEdit === "btn btn-primary active" ? "btn btn-default": "btn btn-primary active";
    $scope.addEdit = $scope.addEdit === true ? false: true;
    $scope.alert = false;
  };

  $scope.addAlert = function(msg, type) {
    $scope.alerts.push({type: type, msg: msg});
  };
  $scope.closeAlert = function(index) {
    $scope.alerts.splice(index, 1);
  };*/

  Measurement.getMeasurements(function(measurements) {
    $scope.measurements = measurements;
  });

  Service.getServices(function(services) {
    $scope.services = services;
  });

  if (meas_id) {
    Measurement.getMeasurement(function(measurement) {
      $scope.measurement = measurement;
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

  /*$scope.viewData = function(event) {
    if (event.$invalid) {
      // If form is invalid, return and let AngularJS show validation errors.
      $scope.addAlert('Invalid form, cannot be submitted', 'danger');
      $scope.alert = true;
      return;
    } else {
      // copy data submitted by form
      $scope.eventData = angular.copy(event);

      var event_type = $scope.eventData.type[0];

      //lookup metadata
      //find data id in metadata
      //get data with id and event type
      //$location.path('/data/' + id);

      // Tell user form has been sent
      $scope.addAlert($scope.eventData.type[0], 'info');
      $scope.alert = true;
    }
  };*/

  /*$scope.measUnchanged = function(measurement) {
    return angular.equals(measurement, $scope.measData);
  };*/

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
      $scope.measData = angular.copy(measurement);

      $scope.measData["status"] = "ON";

      $http({
        method: 'PUT',
        url: '/api/measurements/' + $scope.measData.id,
        data: $scope.measData,
        headers: {'Content-type': 'application/perfsonar+json', 'Content-Length': $scope.measData.length}
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
      $scope.measData = angular.copy(measurement);

      $scope.measData["status"] = "OFF";

      $http({
        method: 'DELETE',
        url: '/api/measurements/' + $scope.measData.id,
        data: $scope.measData,
        headers: {'Content-type': 'application/perfsonar+json', 'Content-Length': $scope.measData.length}
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

  $scope.showDetails = function(id) {
    $location.path('/measurements/' + id);
  };

});
