/*
 * Rest Services for Metadata
 * public/js/services/
 * MetadataService.js
 */

angular.module('MetadataService', []).service('Metadata', function($http) {

  this.getMetadatas = function(metadata) {
    $http.get('/api/metadata')
      .success(function(data) {
        console.log('Request: ' + data);
        metadata(data);
      })
      .error(function(data) {
        console.log('Error: ' + data);
      });
  };

});
