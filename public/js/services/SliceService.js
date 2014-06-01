/*
 * Rest Services for Slice
 * public/js/services/
 * SliceService.js
 */

angular.module('SliceService', []).service('Slice', function($http) {

  this.getSlice = function(sliceInfo) {
    $http.get('/api/slice')
      .success(function(data) {
        console.log('Request: ' + data);
        sliceInfo(data);
      })
      .error(function(data) {
        console.log('Error: ' + data);
      });
  };

});
