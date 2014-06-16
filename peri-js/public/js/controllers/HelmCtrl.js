/*
 * Helm Page Controller
 * public/js/controllers/
 * HelmCtrl.js
 */

angular.module('HelmCtrl', []).controller('HelmController', function($scope, $http, Node, Service, Slice) {

  // scope variables
  $scope.helmData = {};
  $scope.alerts = [];
  $scope.pingData = {};
  $scope.perfData = {};
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

    // default form values
    // $scope.ping.tbtValue = 5;
    // $scope.ping.tbtType = $scope.timeTypes[1];
    // $scope.ping.packetsSent = 1;
    // $scope.ping.tbp = 1;
    // $scope.ping.packetSize = 1000;
    // $scope.ping.reportMS = 10;
    $scope.alert = false;
  };
  $scope.toggleIperf = function() {
    $scope.addPing = false;
    $scope.btnPing = "btn btn-default";
    $scope.btnIperf = $scope.btnIperf === "btn btn-primary active" ? "btn btn-default": "btn btn-primary active";
    $scope.addIperf = $scope.addIperf === true ? false: true;

    // default form values
    // $scope.perf = angular.copy({});
    // $scope.perf.tbtValue = 4;
    // $scope.perf.tbtType = $scope.timeTypes[2];
    // $scope.perf.td = 20;
    // $scope.perf.bt = $scope.bandTesters[0];
    // $scope.perf.proto = $scope.protos[0];
    $scope.alert = false;
  };

  // reset forms to default values we recommend
  $scope.helmReset = function() {
    // clear client and server side form
    // $scope.helmData = {};
    // $scope.helm = angular.copy($scope.helmData);

    // clear client side form and reset defaults
    $scope.helm = angular.copy({});
    $scope.helm.every = 28800;
    $scope.helm.duration = 28799;
    $scope.helm.num = 1;
    $scope.helm.report = 1;
    $scope.helm.size = 10000000;
    $scope.helm.ttl = 1500000;
    $scope.closeAlert(0);
  };

  // compare form data with in memory data
  $scope.helmReset();
  $scope.helmUnchanged = function(helm) {
    return angular.equals(helm, $scope.helmData);
  };

  $scope.helmSubmit = function(helm) {
    if (helm.$invalid) {
      // If form is invalid, return and let AngularJS show validation errors.
      $scope.addAlert('Invalid form, cannot be submitted', 'danger');
      $scope.alert = true;
      return;
    } else {
      // Tell user form has been sent
      // $scope.addAlert('Data sent to UNIS. Please wait for confirmation.', 'info');
      // $scope.alert = true;

      // copy data submitted by form
      $scope.helmData = angular.copy(helm);

      /*var helm_measurement = {
        "$schema": "http://unis.incntre.iu.edu/schema/20140214/measurement#",
        "ts": Math.round(new Date().getTime() / 1000),
        "services": [
          "http://dev.incntre.iu.edu:8888/services/538fce2be7798940fc000117",
          "http://dev.incntre.iu.edu:8888/services/538fc810e7798940fc000091",
          "http://dev.incntre.iu.edu:8888/services/538fc350e7798940fc000003"
        ],
        "eventTypes": [
          "ps:tools:helm"
        ],
        "configuration": {
          "schedule_params": {
            "every": $scope.helm.every,
            "duration":$scope.helm.duration,
            "num_to_schedule":$scope.helm.num
          },
          "reporting_params": $scope.helm.report,
          "collection_size":$scope.helm.size,
          "collection_ttl":$scope.helm.ttl,
          "regex": ",(?P<bandwidth>\\d+)$",
          "probe_module": "cmd_line_probe",
          "collection_schedule":"adaptive.silent_lamb",
          "command": "iperf blah blah",
          "ms_url": "http://localhost:8888",
          "data_file": "/tmp/ops_iperf.log",
          "eventTypes": {
            "bandwidth": "ps:tools:blipp:linux:net:iperf:bandwidth"
          },
          "name": $scope.helm.desc
        }
      };*/

      /*$http({
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
      });*/
    }
  };
}); // end controller
