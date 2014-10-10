/*
 * Rest Services for Depot
 * public/js/services/
 * DepotService.js
 */

angular.module('DepotService', []).service('Depot', function($http, $routeParams, Socket) {

  Socket.emit("depots_request",{});

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
      console.log('HTTP Service Request: ' , data);
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

  this.getMeasurement = function(measurement) {
    $http.get('/api/measurements/' + $routeParams.id)
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

  this.getMetadata = function(metadata) {
    $http.get('/api/metadata/' + $routeParams.id)
      .success(function(data) {
        console.log('Metadata Request: ' + data);
        metadata(data);
      })
      .error(function(data) {
        console.log('Metadata Error: ' + data);
      });
  };

  this.getMetadataData = function(metadataData) {
    var data_id = $routeParams.id;

    $http.get('/api/data/' + data_id).success(function(data) {
      console.log('Data Request: ' + data);
      metadataData(data);

      Socket.on('depots_data',function(data){
        console.log('depots Data Request: ' , data);
        metadataData(data);
      });
    }).error(function(data) {
      console.log('Data Error: ' + data);
    });
  };

});
