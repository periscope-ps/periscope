/*
 * Home Page Controller
 * public/js/controllers/
 * MainCtrl.js
 */

angular.module('MainCtrl', []).controller('MainController', function($scope, $http) {

  $http.get('/api/slice')
    .success(function(data) {
      $scope.gn = data[0].gn_address;
      $scope.slice = data[0].slice;
      $scope.project = data[0].project;
      console.log(data);
    })
    .error(function(data) {
      console.log('Error: ' + data);
    });
});
