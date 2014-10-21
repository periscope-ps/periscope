/*
 * Rest Services for IDMS
 * public/js/services/
 * IdmsService.js
 */

angular.module('IdmsService', []).service('Idms', function($http, Socket) {

  this.getMetadata = function(id, metadata) {
    $http.get('/api/metadata/' + id).success(function(data) {
      console.log('HTTP Metadata Request: ' + data);
      metadata(data);
    }).error(function(data) {
      console.log('HTTP Metadata Error: ' + data);
    });
  };

  this.getData = function(data) {
    Socket.on('data_data',function(data_request) {
      console.log('Incoming Service Depot Data: ' , data_request);
      data(data_request);
    });
  };

  this.getDataId = function(id, metadataData) {
    Socket.emit('data_id_request',{'id': id});

    $http.get('/api/data/' + id).success(function(data) {
      console.log('HTTP Data Request: ' + data);
      metadataData(data);
    }).error(function(data) {
      console.log('HTTP Data Error: ' + data);
    });

    Socket.on('data_id_data', function(data){
      console.log('Incoming IDMS Data ID data: ' , data);
      metadataData(data);
    });
  };

});
