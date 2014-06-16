/*
 * Helm Page Controller
 * public/js/controllers/
 * HelmCtrl.js
 */

angular.module('HelmCtrl', []).controller('HelmController', function($scope, $http, Node, Service, Slice) {

  // scope variables
  $scope.helmFullData = {};
  $scope.alerts = [];
  $scope.timeTypes = [
    {type:'Seconds'},
    {type:'Minutes'},
    {type:'Hours'},
    {type:'Days'}
  ];
  $scope.bandTesters = [
    {type:'Iperf'}
  ];
  $scope.protos = [
    {type:'tcp'},
    {type:'udp'}
  ];

  // load dependent data
  Node.getNodes(function(nodes) {
    $scope.nodes = nodes;
  });
  Slice.getSlice(function(sliceInfo) {
    $scope.geniSlice = sliceInfo[0];
  });
  Service.getServices(function(services) {
    $scope.services = services;
  });

  // global node shouldn't be selectable
  $scope.filterNodes = function(node) {
    if(node.name != 'GN0')
    {
      return true;
    }
    return false;
  };

  // find the service running on a node
  $scope.getNodeService = function(node_ref) {
    for(var i = 0; $scope.services.length; i++) {
      if ($scope.services[i].runningOn.href == node_ref) {
        return $scope.services[i].selfRef;
      }
    }
  };

  // alerts for this scope
  $scope.addAlert = function(msg, type) {
    $scope.alerts.push({type: type, msg: msg});
  };
  $scope.closeAlert = function(index) {
    $scope.alerts.splice(index, 1);
  };

  // load default form data, toggle ui buttons
  $scope.toggleFull = function() {
    $scope.addPartial = false;
    $scope.btnPartial = "btn btn-default";
    $scope.btnFull = $scope.btnFull === "btn btn-primary active" ? "btn btn-default": "btn btn-primary active";
    $scope.addFull = $scope.addFull === true ? false: true;

    // default form values
    $scope.alert = false;
  };
  $scope.togglePartial = function() {
    $scope.addFull = false;
    $scope.btnFull = "btn btn-default";
    $scope.btnPartial = $scope.btnPartial === "btn btn-primary active" ? "btn btn-default": "btn btn-primary active";
    $scope.addPartial = $scope.addPartial === true ? false: true;

    // default form values
    $scope.alert = false;
  };
  $scope.togglePing = function() {
    $scope.addIperf = false;
    $scope.btnIperf = "btn btn-default";
    $scope.btnPing = $scope.btnPing === "btn btn-primary active" ? "btn btn-default": "btn btn-primary active";
    $scope.addPing = $scope.addPing === true ? false: true;

    if ($scope.addFull === true) {
      // default form values
      $scope.helmFull = angular.copy({});
      $scope.helmFull.tbtValue = 5;
      $scope.helmFull.tbtType = $scope.timeTypes[1];
      $scope.helmFull.packetsSent = 1;
      $scope.helmFull.tbp = 1;
      $scope.helmFull.packetSize = 1000;
      $scope.helmFull.reportMS = 10;
    } else if ($scope.addPartial === true) {
      // default form values
      // $scope.helmPartial = angular.copy({});
      // $scope.helmPartial.tbtValue = 5;
      // $scope.helmPartial.tbtType = $scope.timeTypes[1];
      // $scope.helmPartial.packetsSent = 1;
      // $scope.helmPartial.tbp = 1;
      // $scope.helmPartial.packetSize = 1000;
      // $scope.helmPartial.reportMS = 10;
    } else {
      return;
    }

    $scope.alert = false;
  };
  $scope.toggleIperf = function() {
    $scope.addPing = false;
    $scope.btnPing = "btn btn-default";
    $scope.btnIperf = $scope.btnIperf === "btn btn-primary active" ? "btn btn-default": "btn btn-primary active";
    $scope.addIperf = $scope.addIperf === true ? false: true;

    if ($scope.addFull === true) {
      // default form values
      $scope.helmFull = angular.copy({});
      $scope.helmFull.tbtValue = 4;
      $scope.helmFull.tbtType = $scope.timeTypes[2];
      $scope.helmFull.td = 20;
      $scope.helmFull.bt = $scope.bandTesters[0];
      $scope.helmFull.proto = $scope.protos[0];
    } else if ($scope.addPartial === true) {
      // default form values
      // $scope.helmPartial = angular.copy({});
      // $scope.helmPartial.tbtValue = 4;
      // $scope.helmPartial.tbtType = $scope.timeTypes[2];
      // $scope.helmPartial.td = 20;
      // $scope.helmPartial.bt = $scope.bandTesters[0];
      // $scope.helmPartial.proto = $scope.protos[0];
    } else {
      return;
    }

    $scope.alert = false;
  };

  // reset forms to default values we recommend
  $scope.helmReset = function() {
    // clear client and server side form
    // $scope.helmData = {};
    // $scope.helm = angular.copy($scope.helmData);

    if ($scope.addFull === true) {
      if ($scope.addIperf === true) {
        // default form values
        $scope.helmFull = angular.copy({});
        $scope.helmFull.tbtValue = 4;
        $scope.helmFull.tbtType = $scope.timeTypes[2];
        $scope.helmFull.td = 20;
        $scope.helmFull.bt = $scope.bandTesters[0];
        $scope.helmFull.proto = $scope.protos[0];
      } else if ($scope.addPing === true) {
        // default form values
        $scope.helmFull = angular.copy({});
        $scope.helmFull.tbtValue = 5;
        $scope.helmFull.tbtType = $scope.timeTypes[1];
        $scope.helmFull.packetsSent = 1;
        $scope.helmFull.tbp = 1;
        $scope.helmFull.packetSize = 1000;
        $scope.helmFull.reportMS = 10;
      } else {
        return;
      }
    } else if ($scope.addPartial === true) {
      alert("reset partial");
    } else {
      return;
    }

    $scope.closeAlert(0);
  };

  // compare form data with in memory data
  $scope.helmReset();
  $scope.helmFullUnchanged = function(helmFull) {
    return angular.equals(helmFull, $scope.helmFullData);
  };

  $scope.helmFullSubmit = function(helmFull) {
    if (helmFull.$invalid) {
      // If form is invalid, return and let AngularJS show validation errors.
      $scope.addAlert('Invalid form, cannot be submitted', 'danger');
      $scope.alert = true;
      return;
    } else {
      // Tell user form has been sent
      // $scope.addAlert('Data sent to UNIS. Please wait for confirmation.', 'info');
      // $scope.alert = true;

      // copy data submitted by form
      $scope.helmFullData = angular.copy(helmFull);

      if ($scope.addIperf === true) {
        // build ping command from user options
        if ($scope.helmFullData.proto.type == 'udp') {
          var perf_command = "iperf -u -c " + $scope.helmFullData.th + " -t 20 -y C ";
        } else {
          var perf_command = "iperf -c " + $scope.helmFullData.th + " -t 20 -y C ";
        }

        // lookup service running on given node
        var nodeService = $scope.getNodeService($scope.helmFullData.nodes.split(" ")[1]);

        var helm_measurement = {
          $schema: "http://unis.incntre.iu.edu/schema/20140214/measurement#",
          service: nodeService,
          ts: Math.round(new Date().getTime() * 1000),
          participants: [
            {from: "NYC", to: "LA"},
            {from: "LA", to: "NYC"}
          ],
          properties: {
            geni: {
              slice_uuid: $scope.geniSlice.slice_uuid
            }
          },
          eventTypes: [
            "ps:tools:helm"
          ],
          configuration: {
            status: "ON",
            regex: ",(?P<bandwidth>\d+)$",
            window_size: 0,
            protocol: $scope.helmFullData.proto.type,
            probe_module: "cmd_line_probe",
            test_duration: $scope.helmFullData.td,
            schedule_params: {
              every: $scope.helmFullData.tbtValue
            },
            tool: "iperf",
            reporting_params: 1,
            client: null,
            command: perf_command,
            ms_url: $scope.geniSlice.ms_url,
            eventTypes: {
              bandwidth: "ps:tools:blipp:linux:net:iperf:bandwidth"
            },
            udp_bandwidth: 0,
            collection_schedule: "builtins.simple",
            name: $scope.helmFullData.desc
          },
          type: "iperf"
        };
      } else if ($scope.addPing === true) {
        // build ping command from user options
        var ping_command = "ping -c 1 -s " + $scope.helmFullData.packetSize + " -i " + $scope.helmFullData.tbp;

        // lookup service running on given node
        var nodeService = $scope.getNodeService($scope.helmFullData.nodes.split(" ")[1]);

        // build ping measurement to submit
        var helm_measurement = {
          $schema: "http://unis.incntre.iu.edu/schema/20140214/measurement#",
          service: nodeService,
          ts: Math.round(new Date().getTime() * 1000),
          participants: [
            {from: "ATL", to: "SF"},
            {from: "SF", to: "ATL"}
          ],
          properties: {
            geni: {
              slice_uuid: $scope.geniSlice.slice_uuid
            }
          },
          eventTypes: [
            "ps:tools:helm"
          ],
          configuration: {
            status: "ON",
            regex: "ttl=(?P<ttl>\d+).*time=(?P<rtt>\d+\.\d+|\d+)",
            reporting_params: $scope.helmFullData.reportMS,
            probe_module: "cmd_line_probe",
            packet_interval: $scope.helmFullData.pTBP,
            collection_schedule: "builtins.simple",
            packet_size: $scope.helmFullData.packetSize,
            packet_count: 1,
            command: ping_command,
            schedule_params: {
              every: $scope.helmFullData.tbtValue
            },
            collection_size: 100000,
            ms_url: $scope.geniSlice.ms_url,
            eventTypes: {
              rtt: "ps:tools:blipp:linux:net:ping:rtt",
              ttl: "ps:tools:blipp:linux:net:ping:ttl"
            },
            collection_ttl: 1500000,
            name: $scope.helmFullData.desc
          },
          type: "ping"
        };
      } else {
        alert("hit the highway");
        return;
      }

      $http({
        method: 'POST',
        url: '/api/measurements',
        data: helm_measurement,
        headers: {'Content-type': 'application/perfsonar+json'}
      }).
      success(function(data, status, headers, config) {
        // $scope.addAlert(data, 'success');
        // $scope.addAlert(status, 'success');
        // $scope.addAlert(headers, 'success');
        // $scope.addAlert(config, 'success');
        $scope.addAlert('HELM Test: ' + data.configuration.name + ' submitted to UNIS', 'success');
        $scope.alert = true;
      }).
      error(function(data, status, headers, config) {
        // $scope.addAlert(data, 'danger');
        // $scope.addAlert(status, 'danger');
        // $scope.addAlert(headers, 'danger');
        // $scope.addAlert(config, 'danger');
        $scope.addAlert('Status: ' + status.toString() + ', ' + 'Error: ' + data.error.message, 'danger');
        $scope.alert = true;
      });
    }
  };
}); // end controller
