/*
 * Rest Services for IDMS
 * public/js/services/
 * IdmsService.js
 */

angular.module('IdmsService', []).service('Idms', function($http, $routeParams, Socket) {
  Socket.emit("idms_request",{});

  this.getNodes = function(nodes) {
    $http.get('/unis/idms/nodes').success(function(data) {
      console.log('HTTP Node Request: ' , data);
      nodes(data);
    }).error(function(data) {
      console.log('HTTP Node Error: ' , data);
    });
  };

  this.getServices = function(services) {
    $http.get('/unis/idms/services').success(function(data) {
      console.log('Service Request: ' , data);
      services(data);
    }).error(function(data) {
      console.log('HTTP Service Error: ' ,  data);
    });
  };

  this.getMeasurements = function(measurements) {
    $http.get('/unis/idms/measurements/').success(function(data) {
      console.log('Measurement Request: ' + data);
      measurements(data);
    }).error(function(data) {
      console.log('Measurement Error: ' + data);
    });
  };

  this.getMeasurement = function(measurement) {
    $http.get('/unis/idms/measurements/' + $routeParams.id)
      .success(function(data) {
        console.log('Measurement Request: ' + data);
        measurement(data);
      })
      .error(function(data) {
        console.log('Measurement Error: ' + data);
      });
  };

  this.getMetadatas = function(metadata) {
    $http.get('/unis/idms/metadata').success(function(data) {
      console.log('Metadata Request: ' + data);
      metadata(data);
    }).error(function(data) {
      console.log('Metadata Error: ' + data);
    });
  };

  this.getMetadata = function(metadata) {
    $http.get('/unis/idms/metadata/' + $routeParams.id)
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

    $http.get('/unis/idms/data/' + data_id).success(function(data) {
      console.log('Data Request: ' + data);
      metadataData(data);

      Socket.on('idms_data',function(data){
        console.log('IDMS Data Request: ' , data);
        metadataData(data);
      });
    }).error(function(data) {
      console.log('Data Error: ' + data);
    });
  };

});
