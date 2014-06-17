/*
 * Metadata Page Controller
 * public/js/controllers/
 * MetadataCtrl.js
 */

angular.module('MetadataCtrl', []).controller('MetadataController', function($scope, $routeParams, $location, Metadata, Measurement, Node) {

  var metadata_id = $routeParams.id;

  Metadata.getMetadatas(function(metadatas) {
    $scope.metadatas = metadatas;
  });
  Measurement.getMeasurements(function(measurements) {
    $scope.measurements = measurements;
  });
  Node.getNodes(function(nodes) {
    $scope.nodes = nodes;
  });
  if (metadata_id) {
    Metadata.getMetadata(function(metadata) {
      $scope.metadata = metadata;
    });
  }

  $scope.getMetadataMeasurement = function(href) {
    var measurement_id = href.split('/')[4];

    for(var i = 0; $scope.measurements.length; i++) {
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

    for(var i = 0; $scope.nodes.length; i++) {
      if ($scope.nodes[i].id == node_id) {
        return $scope.nodes[i].name;
      }
    }
  };

  $scope.showDetails = function(id) {
    $location.path('/metadata/' + id);
  };
});