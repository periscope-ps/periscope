/*
 * Rest Services for Metadata
 * public/js/services/
 * MetadataService.js
 */

angular.module('MetadataService', []).service('Metadata', function($http, $routeParams) {

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

  this.getMetadata = function(metadata) {
    $http.get('/api/metadata/' + $routeParams.id)
      .success(function(data) {
        console.log('Request: ' + data);
        metadata(data);
      })
      .error(function(data) {
        console.log('Error: ' + data);
      });
  };

  this.getMetadataData = function(metadataData) {
    // for tesing
    var data_id = '539cc241377f972d2e1aa4fb';
    // var data_id = $routeParams.id;

    $http.get('/api/data/' + data_id)
      .success(function(data) {
        console.log('Request: ' + data);
        metadataData(data);
      })
      .error(function(data) {
        console.log('Error: ' + data);
      });
  };

});
