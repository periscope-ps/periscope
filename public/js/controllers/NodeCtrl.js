/*
 * Node Page Controller
 * public/js/controllers/
 * NodeCtrl.js
 */

angular.module('NodeCtrl', []).controller('NodeController', function($scope, $http) {

  $http.get('/api/nodes')
    .success(function(data) {
      $scope.nodes = data;
      console.log(data);
    })
    .error(function(data) {
      console.log('Error: ' + data);
    });

});
