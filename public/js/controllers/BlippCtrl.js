/*
 * Blipp Page Controller
 * public/js/controllers/
 * BlippCtrl.js
 */

angular.module('BlippCtrl', []).controller('BlippController', function($scope, $http, $location) {

  $http.get('/api/nodes')
    .success(function(data) {

      $scope.pingData = {};
      $scope.alerts = [];
      $scope.timeTypes = [
        {type:'Seconds'},
        {type:'Minutes'},
        {type:'Hours'},
        {type:'Days'}
      ];

      /*var ping_measurement = {
        "$schema": "http://unis.incntre.iu.edu/schema/20140214/measurement#",
        "service": "http://localhost:8888/services/MXRRLAWJI94GMEDC",
        "ts": 1398785926407953,
        "eventTypes": [
          "ps:tools:blipp:linux:net:ping:rtt",
          "ps:tools:blipp:linux:net:ping:ttl"
        ],
        "configuration": {
          "regex": "ttl=(?P<ttl>\\d+).*time=(?P<rtt>\\d+\\s|\\d+\\.\\d+)",
          "reporting_params": 1,
          "probe_module": "cmd_line_probe",
          "schedule_params": {
            "every": 5
          },
          "collection_schedule": "builtins.simple",
          "command": "ping -c 1 156.56.5.10",
          "collection_size": 10000000,
          "ms_url": "http://localhost:8888",
          "data_file": "/tmp/ops_ping.log",
          "eventTypes": {
            "rtt": "ps:tools:blipp:linux:net:ping:rtt",
            "ttl": "ps:tools:blipp:linux:net:ping:ttl"
          },
          "collection_ttl": 1500000,
          "name": "ping"
        }
      };*/

      $scope.addAlert = function(msg, type) {
        $scope.alerts.push({type: type, msg: msg});
      };
      $scope.closeAlert = function(index) {
        $scope.alerts.splice(index, 1);
      };
      $scope.pingSubmit = function(ping) {

        if (ping.$invalid) {
          // If form is invalid, return and let AngularJS show validation errors.
          $scope.addAlert('Invalid form, cannot be submitted', 'danger');
          $scope.alert = true;
          return;
        } else {
          // Tell user form has been sent
          // $scope.addAlert('Data sent to UNIS. Please wait for confirmation.', 'info');
          // $scope.alert = true;

          // copy data submitted by form
          $scope.pingData = angular.copy(ping);

          var ping_measurement = {
            "$schema": "http://unis.incntre.iu.edu/schema/20140214/measurement#",
            "service": "http://localhost:8888/services/MXRRLAWJI94GMEDC",
            "ts": 1398785926407953,
            "eventTypes": [
              "ps:tools:blipp:linux:net:ping:rtt",
              "ps:tools:blipp:linux:net:ping:ttl"
            ],
            "configuration": {
              "regex": "ttl=(?P<ttl>\\d+).*time=(?P<rtt>\\d+\\s|\\d+\\.\\d+)",
              "reporting_params": $scope.pingData.reportMS,
              "probe_module": "cmd_line_probe",
              "schedule_params": {
                "every": $scope.pingData.tbtValue
              },
              "collection_schedule": "builtins.simple",
              "command": "ping -c " + $scope.pingData.to,
              "collection_size": $scope.pingData.packetSize,
              "ms_url": "http://localhost:8888",
              "data_file": "/tmp/ops_ping.log",
              "eventTypes": {
                "rtt": "ps:tools:blipp:linux:net:ping:rtt",
                "ttl": "ps:tools:blipp:linux:net:ping:ttl"
              },
              "collection_ttl": 1500000,
              "name": $scope.pingData.desc
            }
          };

          $http({
            method: 'POST',
            url: '/api/measurements',
            data: ping_measurement,
            headers: {'Content-type': 'application/perfsonar+json'}
          }).
          success(function(data, status, headers, config) {
            // $scope.addAlert(data, 'success');
            // $scope.addAlert(status, 'success');
            // $scope.addAlert(headers, 'success');
            // $scope.addAlert(config, 'success');
            var measurement = data;
            $scope.addAlert('BLiPP Test: ' + measurement.configuration.name + ' submitted to UNIS', 'success');
            $scope.alert = true;
          }).
          error(function(data, status, headers, config) {
            // $scope.addAlert(data, 'danger');
            // $scope.addAlert(status, 'danger');
            // $scope.addAlert(headers, 'danger');
            // $scope.addAlert(config, 'danger');
            var measurement = data;
            $scope.addAlert('Status: ' + status.toString() + ', ' + 'Error: ' + measurement.error.message, 'danger');
            $scope.alert = true;
          });
        }
      };
      $scope.pingReset = function() {
        // clear client and server side form
        // $scope.pingData = {};
        // $scope.ping = angular.copy($scope.pingData);

        // clear client side form and reset defaults
        $scope.ping = angular.copy({});
        $scope.ping.tbtValue = 5;
        $scope.ping.tbtType = $scope.timeTypes[1];
        $scope.ping.packetsSent = 1;
        $scope.ping.tbp = 1;
        $scope.ping.packetSize = 1000;
        $scope.ping.reportMS = 10;
        $scope.closeAlert(0);
      };
      $scope.pingReset();
      $scope.pingUnchanged = function(ping) {
        return angular.equals(ping, $scope.pingData);
      };
      $scope.togglePing = function() {
        $scope.addIperf = false;
        $scope.btnIperf = "btn btn-default";
        $scope.addNetlogger = false;
        $scope.btnNetlogger = "btn btn-default";
        $scope.btnPing = $scope.btnPing === "btn btn-primary active" ? "btn btn-default": "btn btn-primary active";
        $scope.addPing = $scope.addPing === true ? false: true;

        // default form values
        $scope.ping.tbtValue = 5;
        $scope.ping.tbtType = $scope.timeTypes[1];
        $scope.ping.packetsSent = 1;
        $scope.ping.tbp = 1;
        $scope.ping.packetSize = 1000;
        $scope.ping.reportMS = 10;
        $scope.alert = false;
      };
      $scope.toggleIperf = function() {
        $scope.addPing = false;
        $scope.btnPing = "btn btn-default";
        $scope.addNetlogger = false;
        $scope.btnNetlogger = "btn btn-default";
        $scope.btnIperf = $scope.btnIperf === "btn btn-primary active" ? "btn btn-default": "btn btn-primary active";
        $scope.addIperf = $scope.addIperf === true ? false: true;
      };
      $scope.toggleNetlogger = function() {
        $scope.addPing = false;
        $scope.btnPing = "btn btn-default";
        $scope.addIperf = false;
        $scope.btnIperf = "btn btn-default";
        $scope.btnNetlogger = $scope.btnNetlogger === "btn btn-primary active" ? "btn btn-default": "btn btn-primary active";
        $scope.addNetlogger = $scope.addNetlogger === true ? false: true;
      };
      $scope.nodes = data;
      $scope.filterNodes = function(node)
      {
          if(node.name != 'GN0')
          {
              return true; // this will be listed in the results
          }
          return false; // otherwise it won't be within the results
      };
    })
    .error(function(data) {
      console.log('Error: ' + data);
    });
});
