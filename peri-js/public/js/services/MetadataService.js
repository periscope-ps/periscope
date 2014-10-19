/*
 * Rest Services for Metadata
 * public/js/services/
 * MetadataService.js
 */

angular.module('MetadataService', []).service('Metadata', function($http, $routeParams, Socket) {
  Socket.emit("metadata_request",{});

  this.getMetadatas = function(metadata) {
    $http.get('/api/metadata').success(function(data) {
      console.log('Metadata Request: ' + data);
      metadata(data);

      Socket.on('metadata_data',function(data){
        console.log('Metadata Service Request: ' , data);
        metadata(data);
      });
    }).error(function(data) {
      console.log('Metadata Error: ' + data);
    });
  };

  this.getMetadata = function(id, metadata) {
    $http.get('/api/metadata/' + id)
      .success(function(data) {
        console.log('Metadata Request: ' + data);
        metadata(data);
      })
      .error(function(data) {
        console.log('Metadata Error: ' + data);
      });
  };

  this.getMetadataData = function(id, metadataData) {
    Socket.emit('data_id_request',{'id': data_id});

    $http.get('/api/data/' + id).success(function(data) {
      console.log('Data Request: ' + data);
      metadataData(data);

      Socket.on('data_id_data',function(data){
        console.log('Data Service Request: ' , data);
        metadataData(data);
      });
    }).error(function(data) {
      console.log('Data Error: ' + data);
    });
  };

});
