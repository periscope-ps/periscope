/*
 * Metadata Page Controller
 * public/js/controllers/
 * MetadataCtrl.js
 */

angular.module('MetadataCtrl', []).controller('MetadataController', function($scope, $routeParams, $location, Metadata, Measurement, Node) {

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

  if (metadata_id) {
    Metadata.getMetadataData(function(metadataData) {
      $scope.metadataData = $scope.metadataData || [];

      if (typeof metadataData =='string')
        metadataData = JSON.parse(metadataData);

      $scope.metadataData = $scope.metadataData.concat(metadataData);

      Metadata.getMetadata(function(metadata) {
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
    var node_id = href.split('/')[4];

    for(var i = 0; i < $scope.nodes.length; i++) {
      if ($scope.nodes[i].id == node_id) {
        return $scope.nodes[i].name;
      }
    }
  };

  $scope.showMetadataData = function(metadata_id) {
    $location.path('/metadata/' + metadata_id);
  };
});
