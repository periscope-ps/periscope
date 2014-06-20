/*
 * Rest Services for Help
 * public/js/services/
 * HelpService.js
 */

angular.module('HelpService', []).service('Help', function($http) {

  this.getHelp = function(helpMe) {
    $http.get('/api/help')
      .success(function(data) {
        console.log('Help Request: ' + data);
        helpMe(data);
      })
      .error(function(data) {
        console.log('Help Error: ' + data);
      });
  };

});
