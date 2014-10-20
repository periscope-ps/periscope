/*
 * Rest Services for Metadata
 * public/js/services/
 * MetadataService.js
 */

angular.module('MetadataService', []).service('Metadata', function($http, $routeParams, Socket) {
  Socket.emit("metadata_request",{});

  this.getMetadatas = function(metadata) {
    $http.get('/api/metadata').success(function(data) {
      console.log('HTTP Metadata Request: ' + data);
      metadata(data);

      Socket.on('metadata_data',function(data){
        console.log('Incoming Metadata Data: ' , data);
        metadata(data);
      });
    }).error(function(data) {
      console.log('HTTP Metadata Error: ' + data);
    });
  };

  this.getMetadata = function(id, metadata) {
    $http.get('/api/metadata/' + id)
      .success(function(data) {
        console.log('HTTP Metadata Request: ' + data);
        metadata(data);
      })
      .error(function(data) {
        console.log('HTTP Metadata Error: ' + data);
      });
  };

  this.getDataId = function(id, metadataData) {
    Socket.emit('data_id_request',{'id': id});

    $http.get('/api/data/' + id).success(function(data) {
      console.log('HTTP Data ID Request: ' + data);
      metadataData(data);

      Socket.on('data_id_data',function(data){
        console.log('Incoming Data ID Data: ' , data);
        metadataData(data);
      });
    }).error(function(data) {
      console.log('HTTP Data Error: ' + data);
    });
  };

});
