/*
 * Rest Services for IDMS
 * public/js/services/
 * IdmsService.js
 */

angular.module('IdmsService', []).service('Idms', function($http, $routeParams, Socket) {

  this.getNodes = function(nodes) {
    $http.get('/api/nodes').success(function(data) {
      console.log('HTTP Node Request: ' , data);
      nodes(data);
    }).error(function(data) {
      console.log('HTTP Node Error: ' , data);
    });
  };

  this.getServices = function(services) {
    $http.get('/api/services').success(function(data) {
      console.log('Service Request: ' , data);
      services(data);
    }).error(function(data) {
      console.log('HTTP Service Error: ' ,  data);
    });
  };

  this.getMeasurements = function(measurements) {
    $http.get('/api/measurements/').success(function(data) {
      console.log('Measurement Request: ' + data);
      measurements(data);
    }).error(function(data) {
      console.log('Measurement Error: ' + data);
    });
  };

  this.getMeasurement = function(id, measurement) {
    $http.get('/api/measurements/' + id)
      .success(function(data) {
        console.log('Measurement Request: ' + data);
        measurement(data);
      })
      .error(function(data) {
        console.log('Measurement Error: ' + data);
      });
  };

  this.getMetadatas = function(metadata) {
    $http.get('/api/metadata').success(function(data) {
      console.log('Metadata Request: ' + data);
      metadata(data);
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
    Socket.emit('data_id_request',{id: id});

    $http.get('/api/data/' + id).success(function(data) {
      console.log('Data Request: ' + data);
      metadataData(data);

      Socket.on('data_id_data', function(data){
        console.log('Incoming IDMS Data: ' , data);
        metadataData(data);
      });
    }).error(function(data) {
      console.log('Data Error: ' + data);
    });
  };

});
