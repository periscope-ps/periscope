/*
 * IDMS Page Controller
 * public/js/controllers/
 * IdmsCtrl.js
 */

angular.module('IdmsCtrl', []).controller('IdmsController', function($scope, $routeParams, $location, $timeout, $window, Idms) {

  // var metadata_id = $routeParams.id;
  $scope.addGraph = false;

  Idms.getNodes(function(nodes) {
    $scope.nodes = $scope.nodes || [];

    if (typeof nodes =='string')
      nodes = JSON.parse(nodes);

    $scope.nodes = $scope.nodes.concat(nodes);
  });

  Idms.getServices(function(services) {
    $scope.services = $scope.services || [];

    if (typeof services =='string')
      services = JSON.parse(services);

    $scope.services = $scope.services.concat(services);

    // set timer value
    $scope.onTimeout = function(){
      for(var i = 0; i < $scope.services.length; i++) {
        if($scope.services[i].ttl <= 0) {
          $scope.services[i].status = 'Unknown';
        } else {
          $scope.services[i].ttl--;
        }
      }
      //continue timer
      timeout = $timeout($scope.onTimeout,1000);
    }
    // start timer
    var timeout = $timeout($scope.onTimeout,1000);
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

  /*if (metadata_id) {
    var arrayData = [];
    $scope.addGraph = false;

    Idms.getMetadataData(metadata_id, function(metadataData) {
      $scope.metadataData = $scope.metadataData || [];

      if (typeof metadataData =='string')
        metadataData = JSON.parse(metadataData);

      $scope.metadataData = $scope.metadataData.concat(metadataData);

      Idms.getMetadata(metadata_id, function(metadata) {
        $scope.eventType = metadata.eventType;
      });

      angular.forEach($scope.metadataData, function(key, value) {
        arrayData.push([key.ts, key.value]);
      });

      $scope.graphData = [
      {
        "key": "Data Point",
        "values": arrayData
      }];
      $scope.addGraph = true;
    });
  }*/

  $scope.getServiceNode = function(accessPoint) {
    var ip = accessPoint.split(':')[1].replace('//', '');

    for(var i = 0; i < $scope.nodes.length; i++) {
      if ($scope.nodes[i].properties.geni.logins[0].hostname == ip) {
          return $scope.nodes[i].id;
      } else {
        return 'Node Unknown';
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
    // $location.path('/idms/' + metadata_id);

     if (metadata_id) {
      var arrayData = [];
      $scope.addGraph = false;
      $scope.metadataData = [];
      $scope.graphMetadata = [];

      Idms.getMetadataData(metadata_id, function(metadataData) {
        $scope.metadataData = $scope.metadataData || [];

        if (typeof metadataData =='string')
          metadataData = JSON.parse(metadataData);

        $scope.metadataData = $scope.metadataData.concat(metadataData);

        Idms.getMetadata(metadata_id, function(metadata) {
          $scope.graphMetadata = metadata;
        });

        angular.forEach($scope.metadataData, function(key, value) {
          arrayData.push([key.ts, key.value]);
        });

        $scope.graphData = [
        {
          "key": "Data Point",
          "values": arrayData
        }];
        $scope.addGraph = true;
        $window.scrollTo(0,0);
      });
    }
  };
});
