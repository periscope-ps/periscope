/*
 * Metadata Page Controller
 * public/js/controllers/
 * MetadataCtrl.js
 */

angular.module('MetadataCtrl', []).controller('MetadataController', function($scope, $routeParams, $location, Metadata, Measurement, Node, Service) {

  var metadata_id = $routeParams.id;

  Metadata.getMetadatas(function(metadatas) {
    $scope.metadatas = $scope.metadatas || [];

    if (typeof metadatas =='string')
      metadatas = JSON.parse(metadatas);

    $scope.metadatas = $scope.metadatas.concat(metadatas);
  });

  Measurement.getMeasurements(function(measurements) {
    $scope.measurements = $scope.measurements || [];

    if (typeof measurements =='string')
      measurements = JSON.parse(measurements);

    $scope.measurements = $scope.measurements.concat(measurements);
  });

  Node.getNodes(function(nodes) {
    $scope.nodes = $scope.nodes || [];

    if (typeof nodes =='string')
      nodes = JSON.parse(nodes);

    $scope.nodes = $scope.nodes.concat(nodes);
  });

  Service.getServices(function(services) {
    $scope.services = $scope.services || [];

    if (typeof services =='string')
      services = JSON.parse(services);

    $scope.services = $scope.services.concat(services);
  });

  if (metadata_id) {
    Metadata.getDataId(metadata_id, function(data) {
      $scope.data = $scope.data || [];

      if (typeof data =='string')
        data = JSON.parse(data);

      $scope.data = $scope.data.concat(data);

      Metadata.getMetadata(metadata_id, function(metadata) {
        $scope.eventType = metadata.eventType;
      });

      var arrayData = [];
      angular.forEach($scope.data, function(key, value) {
        arrayData.push([key.ts, key.value]);
      });

      $scope.xAxisTickFormat_Date_Format = function(){
        return function(d){
          var ts = d/1e3;
          return d3.time.format('%X')(new Date(ts));
        }
      };

      $scope.graphData = [
      {
        "key": "Data Point",
        "values": arrayData
      }];
    });
  }

  $scope.getMetadataMeasurement = function(href) {
    var measurement_id = href.split('/')[4];

    for(var i = 0; i < $scope.measurements.length; i++) {
      if ($scope.measurements[i].id == measurement_id) {
        return $scope.measurements[i].configuration.name;
      }
    }
  };

  $scope.getMetadataMeasurementID = function(href) {
    return href.split('/')[4];
  };

  $scope.getMetadataNode = function(href) {
    var measurement_id = href.split('/')[4];

    for(var i = 0; i < $scope.measurements.length; i++) {
      if($scope.measurements[i].id == measurement_id) {
        var service_id = $scope.measurements[i].service.split('/')[4];

        for(var i = 0; i < $scope.services.length; i++) {
          if ($scope.services[i].id == service_id) {
            var node_id = $scope.services[i].runningOn.href.split('/')[4];

            for(var i = 0; i < $scope.nodes.length; i++) {
              if ($scope.nodes[i].id == node_id) {
                  return $scope.nodes[i].name;
              }
            }
          }
        }
      }
    }
  };

  $scope.showData = function(metadata_id) {
    $location.path('/metadata/' + metadata_id);
  };
});
