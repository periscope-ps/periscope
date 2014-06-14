/*
 * Blipp Page Controller
 * public/js/controllers/
 * BlippCtrl.js
 */

angular.module('BlippCtrl', []).controller('BlippController', function($scope, $http) {

  $http.get('/api/nodes')
    .success(function(data) {

      $scope.pingData = {};
      $scope.owpData = {};
      $scope.perfData = {};
      $scope.netlogData = {};
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
        {type:'TCP'},
        {type:'UDP'}
      ];

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
            "service": "http://dev.incntre.iu.edu:8888/services/538fce2be7798940fc000117",
            "ts": Math.round(new Date().getTime() / 1000),
            "eventTypes": [
              "ps:tools:blipp:linux:net:ping:rtt",
              "ps:tools:blipp:linux:net:ping:ttl"
            ],
            "configuration": {
              "status": "ON",
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
      $scope.owpSubmit = function(owp) {

        if (owp.$invalid) {
          // If form is invalid, return and let AngularJS show validation errors.
          $scope.addAlert('Invalid form, cannot be submitted', 'danger');
          $scope.alert = true;
          return;
        } else {
          // Tell user form has been sent
          // $scope.addAlert('Data sent to UNIS. Please wait for confirmation.', 'info');
          // $scope.alert = true;

          // copy data submitted by form
          $scope.owpData = angular.copy(owp);

          var owp_measurement = {
            "$schema": "http://unis.incntre.iu.edu/schema/20140214/measurement#",
            "service": "http://dev.incntre.iu.edu:8888/services/538fc810e7798940fc000091",
            "ts": Math.round(new Date().getTime() / 1000),
            "eventTypes": [
              // "ps:tools:blipp:linux:net:ping:owt",
              // "ps:tools:blipp:linux:net:ping:ttl"
            ],
            "configuration": {
              // "regex": "ttl=(?P<ttl>\\d+).*time=(?P<rtt>\\d+\\s|\\d+\\.\\d+)",
              // "reporting_params": $scope.pingData.reportMS,
              // "probe_module": "cmd_line_probe",
              "schedule_params": {
                // "every": $scope.pingData.tbtValue
              },
              "collection_schedule": "builtins.simple",
              // "command": "ping -c " + $scope.pingData.to,
              // "collection_size": $scope.pingData.packetSize,
              "ms_url": "http://localhost:8888",
              // "data_file": "/tmp/ops_ping.log",
              "eventTypes": {
                // "rtt": "ps:tools:blipp:linux:net:ping:rtt",
                // "ttl": "ps:tools:blipp:linux:net:ping:ttl"
              },
              // "collection_ttl": 1500000,
              "name": $scope.owpData.desc
            }
          };

          $http({
            method: 'POST',
            url: '/api/measurements',
            data: owp_measurement,
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
      $scope.perfSubmit = function(perf) {

        if (perf.$invalid) {
          // If form is invalid, return and let AngularJS show validation errors.
          $scope.addAlert('Invalid form, cannot be submitted', 'danger');
          $scope.alert = true;
          return;
        } else {
          // Tell user form has been sent
          // $scope.addAlert('Data sent to UNIS. Please wait for confirmation.', 'info');
          // $scope.alert = true;

          // copy data submitted by form
          $scope.perfData = angular.copy(perf);

          var perf_measurement = {
            "$schema": "http://unis.incntre.iu.edu/schema/20140214/measurement#",
            "service": "http://dev.incntre.iu.edu:8888/services/538fc810e7798940fc000091",
            "ts": Math.round(new Date().getTime()),
            "eventTypes": [
              "ps:tools:blipp:linux:net:iperf:bandwidth"
            ],
            "configuration": {
              "regex": ",(?P<bandwidth>\\d+)$",
              "probe_module": "cmd_line_probe",
              "collection_schedule": "builtins.simple",
              "command": "iperf " + $scope.perfData.th,
              "ms_url": "http://localhost:8888",
              "data_file": "/tmp/ops_iperf.log",
              "eventTypes": {
                "bandwidth": "ps:tools:blipp:linux:net:iperf:bandwidth"
              },
              "name": $scope.perfData.desc
            }
          };

          $http({
            method: 'POST',
            url: '/api/measurements',
            data: perf_measurement,
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
      $scope.netlogSubmit = function(netlog) {

        if (netlog.$invalid) {
          // If form is invalid, return and let AngularJS show validation errors.
          $scope.addAlert('Invalid form, cannot be submitted', 'danger');
          $scope.alert = true;
          return;
        } else {
          // Tell user form has been sent
          // $scope.addAlert('Data sent to UNIS. Please wait for confirmation.', 'info');
          // $scope.alert = true;

          // copy data submitted by form
          $scope.netlogData = angular.copy(netlog);

          var netlog_measurement = {
            "$schema": "http://unis.incntre.iu.edu/schema/20140214/measurement#",
            "service": "http://dev.incntre.iu.edu:8888/services/538fc350e7798940fc000003",
            "ts": Math.round(new Date().getTime() / 1000),
            "eventTypes": [
              "ps:tools:blipp:linux:net:netlogger:probe"
            ],
            "configuration": {
              "unis_url": "http://localhost:8888",
              "probe_defaults": {
                "ms_url": "http://localhost:8888",
                "collection_schedule": "builtins.simple",
                "schedule_params": {"every": $scope.netlogData.tbrValue}
              },
              "probes":{
                "nl_probe": {
                  "probe_module": "netlogger_probe",
                  "data_file": $scope.netlog.file,
                  "logfile": "/tmp/nl.log",
                  "reporting_params": $scope.netlogData.reportMS
                }
              },
              "name": $scope.netlogData.desc
            }
          };

          $http({
            method: 'POST',
            url: '/api/measurements',
            data: netlog_measurement,
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
      $scope.owpReset = function() {
        // clear client and server side form
        // $scope.pingData = {};
        // $scope.ping = angular.copy($scope.pingData);

        // clear client side form and reset defaults
        // $scope.ping = angular.copy({});
        // $scope.ping.tbtValue = 5;
        // $scope.ping.tbtType = $scope.timeTypes[1];
        // $scope.ping.packetsSent = 1;
        // $scope.ping.tbp = 1;
        // $scope.ping.packetSize = 1000;
        // $scope.ping.reportMS = 10;
        // $scope.closeAlert(0);
      };
      $scope.perfReset = function() {
        // clear client and server side form
        // $scope.perfData = {};
        // $scope.perf = angular.copy($scope.perfData);

        // clear client side form and reset defaults
        $scope.perf = angular.copy({});
        $scope.perf.tbtValue = 4;
        $scope.perf.tbtType = $scope.timeTypes[2];
        $scope.perf.td = 20;
        $scope.perf.bt = $scope.bandTesters[0];
        $scope.perf.proto = $scope.protos[0];
        $scope.closeAlert(0);
      };
      $scope.netlogReset = function() {
        // clear client and server side form
        // $scope.netlogData = {};
        // $scope.netlog = angular.copy($scope.netlogData);

        // clear client side form and reset defaults
        $scope.netlog = angular.copy({});
        $scope.netlog.tbrValue = 5;
        $scope.netlog.tbrType = $scope.timeTypes[0];
        $scope.netlog.reportMS = 10;
        $scope.closeAlert(0);
      };
      $scope.pingReset();
      $scope.pingUnchanged = function(ping) {
        return angular.equals(ping, $scope.pingData);
      };
      $scope.owpReset();
      $scope.owpUnchanged = function(owp) {
        return angular.equals(owp, $scope.owpData);
      };
      $scope.perfReset();
      $scope.perfUnchanged = function(perf) {
        return angular.equals(perf, $scope.perfData);
      };
      $scope.netlogReset();
      $scope.netlogUnchanged = function(netlog) {
        return angular.equals(netlog, $scope.netlogData);
      };
      $scope.togglePing = function() {
        $scope.addOWPing = false;
        $scope.btnOWPing = "btn btn-default";
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
      $scope.toggleOWPing = function() {
        $scope.addPing = false;
        $scope.btnPing = "btn btn-default";
        $scope.addIperf = false;
        $scope.btnIperf = "btn btn-default";
        $scope.addNetlogger = false;
        $scope.btnNetlogger = "btn btn-default";
        $scope.btnOWPing = $scope.btnOWPing === "btn btn-primary active" ? "btn btn-default": "btn btn-primary active";
        $scope.addOWPing = $scope.addOWPing === true ? false: true;

        // default form values
        // $scope.ping.tbtValue = 5;
        // $scope.ping.tbtType = $scope.timeTypes[1];
        // $scope.ping.packetsSent = 1;
        // $scope.ping.tbp = 1;
        // $scope.ping.packetSize = 1000;
        // $scope.ping.reportMS = 10;
        // $scope.alert = false;
      };
      $scope.toggleIperf = function() {
        $scope.addPing = false;
        $scope.btnPing = "btn btn-default";
        $scope.addOWPing = false;
        $scope.btnOWPing = "btn btn-default";
        $scope.addNetlogger = false;
        $scope.btnNetlogger = "btn btn-default";
        $scope.btnIperf = $scope.btnIperf === "btn btn-primary active" ? "btn btn-default": "btn btn-primary active";
        $scope.addIperf = $scope.addIperf === true ? false: true;

        // default form values
        $scope.perf = angular.copy({});
        $scope.perf.tbtValue = 4;
        $scope.perf.tbtType = $scope.timeTypes[2];
        $scope.perf.td = 20;
        $scope.perf.bt = $scope.bandTesters[0];
        $scope.perf.proto = $scope.protos[0];
        $scope.alert = false;
      };
      $scope.toggleNetlogger = function() {
        $scope.addPing = false;
        $scope.btnPing = "btn btn-default";
        $scope.addOWPing = false;
        $scope.btnOWPing = "btn btn-default";
        $scope.addIperf = false;
        $scope.btnIperf = "btn btn-default";
        $scope.btnNetlogger = $scope.btnNetlogger === "btn btn-primary active" ? "btn btn-default": "btn btn-primary active";
        $scope.addNetlogger = $scope.addNetlogger === true ? false: true;

        // default form values
        $scope.netlog = angular.copy({});
        $scope.netlog.tbrValue = 5;
        $scope.netlog.tbrType = $scope.timeTypes[0];
        $scope.netlog.reportMS = 10;
        $scope.alert = false;
      };
      $scope.nodes = data;
      $scope.filterNodes = function(node) {
        if(node.name != 'GN0')
        {
          return true;
        }
        return false;
      };
    })
    .error(function(data, status) {
      console.log('Error: ' + data);
      var error = data;
      $scope.addAlert('Status: ' + status.toString() + ', ' + 'Error: ' + error.error.message, 'danger');
      $scope.alert = true;
    });
});
