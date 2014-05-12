/*
 * Service Page Controller
 * public/js/controllers/
 * ServiceCtrl.js
 */

angular.module('ServiceCtrl', []).controller('ServiceController', function($scope, $http) {

  $http.get('/services')
    .success(function(data) {
      $scope.services = data;
      console.log(data);
    })
    .error(function(data) {
      console.log('Error: ' + data);
    });

});