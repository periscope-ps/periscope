/*
 * IDMS Page Controller
 * public/js/controllers/
 * IdmsCtrl.js
 */

angular.module('IdmsCtrl', []).controller('IdmsController', function($scope, $routeParams, $location, Idms) {

  var metadata_id = $routeParams.id;

  Idms.getNodes(function(nodes) {
    $scope.nodes = $scope.nodes || [];

    if (typeof nodes =='string')
      nodes = JSON.parse(nodes);

    $scope.nodes = $scope.nodes.concat(nodes);
  });

  Idms.getServices(function(services) {
	// Need this services for the map as well -- Yes i am pollution the global scope , will find a better way later 
    $rootScope.idmsServices = $scope.services = $scope.services || $rootScope.idmsServices || [];

    if (typeof services =='string')
      services = JSON.parse(services);

    $rootScope.idmsServices = $scope.services = $scope.services.concat(services);
  });

  Idms.getMeasurements(function(measurements) {
    $scope.measurements = $scope.measurements || [];

    if (typeof measurements =='string')
      measurements = JSON.parse(measurements);

    $scope.measurements = $scope.measurements.concat(measurements);
  });

  Idms.getMetadatas(function(metadata) {
    $scope.metadata = $scope.metadata || [];

    if (typeof metadata =='string')
      metadata = JSON.parse(metadata);

    $scope.metadata = $scope.metadata.concat(metadata);
  });

  if (metadata_id) {
    Idms.getMetadataData(function(metadataData) {
      $scope.metadataData = $scope.metadataData || [];

      if (typeof metadataData =='string')
        metadataData = JSON.parse(metadataData);

      $scope.metadataData = $scope.metadataData.concat(metadataData);

      Idms.getMetadata(function(metadata) {
        $scope.eventType = metadata.eventType;
      });

      var arrayData = [];
      angular.forEach($scope.metadataData, function(key, value) {
        arrayData.push([key.ts, key.value]);
      });

      $scope.graphData = [
      {
        "key": "Data Point",
        "values": arrayData
      }];
    });
  }

  $scope.getServiceNode = function(accessPoint) {
    var ip = accessPoint.split(':')[1].replace('//', '');

    for(var i = 0; i < $scope.nodes.length; i++) {
      if ($scope.nodes[i].properties.geni.logins[0].hostname == ip) {
          return $scope.nodes[i].id;
      }
    }
  };
  $scope.getServiceMeasurement = function(accessPoint) {
    var ip = accessPoint.split(':')[1].replace('//', '');

    for(var i = 0; i < $scope.measurements.length; i++) {
      if($scope.measurements[i].configuration.command) {
        if($scope.measurements[i].configuration.command.split(" ")[1] == ip) {
          return $scope.measurements[i].eventTypes;
        }
      }
    }
  };
  $scope.getServiceMetadata = function(accessPoint) {
    var ip = accessPoint.split(':')[1].replace('//', '');
    var metadatas = [];

    for(var i = 0; i < $scope.measurements.length; i++) {
      if($scope.measurements[i].configuration.command) {
        if($scope.measurements[i].configuration.command.split(" ")[1] == ip) {
          for(var j = 0; j < $scope.metadata.length; j++) {
            if($scope.metadata[j].parameters.measurement.href.split('/')[4] == $scope.measurements[i].id) {
              metadatas.push($scope.metadata[j].id);
            }
          }
        }
      }
    }
    return metadatas;
  };

  $scope.showData = function(metadata_id) {
    $location.path('/idms/' + metadata_id);
  };
});
