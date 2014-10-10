/*
 * Depot Page Controller
 * public/js/controllers/
 * DepotCtrl.js
 */

angular.module('DepotCtrl', []).controller('DepotController', function($scope, $routeParams, $location, Depot) {

  var metadata_id = $routeParams.id;

  Depot.getNodes(function(nodes) {
    $scope.nodes = $scope.nodes || [];

    if (typeof nodes =='string')
      nodes = JSON.parse(nodes);

    $scope.nodes = $scope.nodes.concat(nodes);
  });

  Depot.getServices(function(services) {
    $scope.services = $scope.services || [];

    if (typeof services =='string')
      services = JSON.parse(services);

    $scope.services = $scope.services.concat(services);
  });

  Depot.getMeasurements(function(measurements) {
    $scope.measurements = $scope.measurements || [];

    if (typeof measurements =='string')
      measurements = JSON.parse(measurements);

    $scope.measurements = $scope.measurements.concat(measurements);
  });

  Depot.getMetadatas(function(metadata) {
    $scope.metadata = $scope.metadata || [];

    if (typeof metadata =='string')
      metadata = JSON.parse(metadata);

    $scope.metadata = $scope.metadata.concat(metadata);
  });

  if (metadata_id) {
    Depot.getMetadataData(function(metadataData) {
      $scope.metadataData = $scope.metadataData || [];

      if (typeof metadataData =='string')
        metadataData = JSON.parse(metadataData);

      $scope.metadataData = $scope.metadataData.concat(metadataData);

      Depot.getMetadata(function(metadata) {
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
    $location.path('/depots/' + metadata_id);
  };

});
