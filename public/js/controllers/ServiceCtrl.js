/*
 * Service Page Controller
 * public/js/controllers/
 * ServiceCtrl.js
 */

angular.module('ServiceCtrl', []).controller('ServiceController', function($scope, Service) {

  Service.getServices(function(services) {
    $scope.services = services;
  });

});
