/*
 * Help Page Controller
 * public/js/controllers/
 * HelpCtrl.js
 */

angular.module('HelpCtrl', []).controller('HelpController', function($scope, Help) {

  Help.getHelp(function(helpMe) {
    $scope.helps = helpMe;
  });

});
