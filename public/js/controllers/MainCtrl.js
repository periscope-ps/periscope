/*
 * Home Page Controller
 * public/js/controllers/
 * MainCtrl.js
 */

angular.module('MainCtrl', []).controller('MainController', function($scope, $http) {

  $http.get('/api/slice')
    .success(function(data) {
      console.log(data);
      $scope.exAddy = data[0].external_address;
      $scope.gn = data[0].gn_address;
      $scope.unis = data[0].unis_instance;
      $scope.ms = data[0].ms_url;
      $scope.project = data[0].project;
      $scope.slice = data[0].slice;
      $scope.uuid = data[0].slice_uuid;
    })
    .error(function(data) {
      console.log('Error: ' + data);
    });
});
