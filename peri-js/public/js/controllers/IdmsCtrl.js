/*
 * IDMS Page Controller
 * public/js/controllers/
 * IdmsCtrl.js
 */

angular.module('IdmsCtrl', []).controller('IdmsController', function($scope, $routeParams, $location, $rootScope, Idms, Socket) {

  var SHOW_ETS = ['ps:tools:blipp:ibp_server:resource:usage:used',
                  'ps:tools:blipp:ibp_server:resource:usage:free',
                  'ps:tools:blipp:linux:cpu:utilization:user',
                  'ps:tools:blipp:linux:cpu:utilization:system'];

  var metadata_id = $routeParams.id;

  // place inital app data into scope for view
  $scope.services = $rootScope.services;
  $scope.measurements = $rootScope.measurements;
  $scope.metadata = $rootScope.metadata;
  $scope.nodes = $rootScope.nodes;
  $scope.ports = $rootScope.ports;

  $scope.addGraph = false;

  // continue to listen for new data
  Socket.on('service_data', function(data) {

    if (typeof data =='string') {
      data = JSON.parse(data);
    }

    // data.status = 'New';
    console.log('Socket Service Request: ', data);

    var now = Math.round(new Date().getTime() / 1e3) //seconds
    data.ttl = Math.round(((data.ttl + (data.ts / 1e6)) - now));

    function searchServices(addService) {
      console.log("searchServices function");

      // search for duplicate id's
      for(var i = 0; $scope.services.length; i++) {

        if($scope.services[i].accessPoint == data.accessPoint) {
          // $scope.services[i].ttl = -1;
          console.log("removing: " + $scope.services[i].accessPoint + " ts: " + $scope.services[i].ts);
          $scope.services.splice(i, 1);
          break;
        }
      }

      // Call the callback
      addService();
    }

    function addService() {
      console.log("addService callback");

      // add new data to scope for view
      $scope.services.push(data);
    }

    searchServices(addService);
  });

  if (metadata_id) {
    Idms.getDataId(metadata_id, function(data) {
      $scope.data = $scope.data || [];

      if (typeof data =='string')
        data = JSON.parse(data);

      $scope.data = $scope.data.concat(data);

      Idms.getMetadata(metadata_id, function(metadata) {
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

      $scope.yAxisFormatFunction = function(){
        return function(d){
          return (d/1e9).toFixed(2); // GB
        }
      };

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
      } else {
        return 'Node Unknown';
      }
    }
  };

  $scope.getMetadataShortET = function(md) {
    var arr = md.eventType.split(':');
    return arr.pop();
  };

  $scope.getServiceMeasurement = function(sref) {
    for(var i = 0; i < $scope.measurements.length; i++) {
      if($scope.measurements[i].service == sref) {
        return $scope.measurements[i].eventTypes;
      }
    }
  };

  $scope.getServiceMetadata = function(service) {
    var metadatas = [];
    var seen_ets = [];

    // this case is brutal because our metadata is missing subject hrefs
    // perhaps can fix in blipp for IDMS
    if (service.serviceType == 'ibp_server') {
      var ip = service.accessPoint.split(':')[1].replace('//', '');
      for (var i = 0; i < $scope.measurements.length; i++) {
        if ($scope.measurements[i].configuration.command) {
          if ($scope.measurements[i].configuration.command.split(" ")[1] == ip) {
            for (var j = 0; j < $scope.metadata.length; j++) {
              if ((seen_ets.indexOf($scope.metadata[j].eventType) == -1) &&
                  ($scope.metadata[j].parameters.measurement.href.split('/')[4] == $scope.measurements[i].id)) {
                    metadatas.push($scope.metadata[j]);
                    seen_ets.push($scope.metadata[j].eventType);
              }
            }
          }
        }
      }
    } else {
      for (var i = 0; i < $scope.measurements.length; i++) {
        if ($scope.measurements[i].service == service.selfRef) {
          for (var j = 0; j < $scope.metadata.length; j++) {
            if ($scope.metadata[j].parameters.measurement.href == $scope.measurements[i].selfRef) {
              if ((seen_ets.indexOf($scope.metadata[j].eventType) == -1) &&
                  (SHOW_ETS.indexOf($scope.metadata[j].eventType) >= 0)) {
                    metadatas.push($scope.metadata[j]);
                    seen_ets.push($scope.metadata[j].eventType);
              }
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

  $scope.showMap = function(service_id) {
    $location.path('/idmsMap/' + service_id);
  };
});
