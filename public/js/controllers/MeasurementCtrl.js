/*
 * Measurement Page Controller
 * public/js/controllers/
 * MeasurementCtrl.js
 */

angular.module('MeasurementCtrl', []).controller('MeasurementController', function($scope, $http) {

  $http.get('/measurements')
    .success(function(data) {
      var measurements = data;
      /*var length = measurements.length();

      for(int i; i < length; i++) {
        $scope.name = measurements[i].configuration.name
        $scope.selfRef = measurements[i].
        $scope.ts = measurements[i].ts
      }*/


      $scope.measurements = measurements;

      console.log(data);
    })
    .error(function(data) {
      console.log('Error: ' + data);
    });

});
