/*
 * Blipp Page Controller
 * public/js/controllers/
 * BlippCtrl.js
 */

angular.module('BlippCtrl', []).controller('BlippController', function($scope, $http) {

  $http.get('/nodes')
    .success(function(data) {

      $scope.pingData = {};

      $scope.pingSubmit = function(ping) {
        $scope.pingData = angular.copy(ping);

        // process and submit data below
        //
      };
      $scope.pingReset = function() {
        // clear client and server side form
        // $scope.pingData = {};
        // $scope.ping = angular.copy($scope.pingData);

        // clear client side form and reset defaults
        $scope.ping = angular.copy({});
        $scope.ping.packetsSent = 1;
      };
      $scope.pingUnchanged = function(ping) {
        return angular.equals(ping, $scope.pingData);
      };

      $scope.pingReset();

      // $scope.submitPing = function(ping) {

        /*var ping = {
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
              "name": "ops_ping"
            }
        };*/

        // alert(ping);

        /*http({
          method  : 'POST',
          url     : 'http://localhost:8888/measurements',
          data    : $.param(ping),
          headers : { 'Content-Type': 'application/json' }
        })
        .success(function(data) {
          if (!data.success) {
            alert("error");
          } else {
            $scope.pingSuccess = true;
            $scope.message = data.message;
          }
        });*/

      // };

      $scope.togglePing = function() {
        $scope.addIperf = false;
        $scope.btnIperf = "btn btn-default";
        $scope.addNetlogger = false;
        $scope.btnNetlogger = "btn btn-default";
        $scope.btnPing = $scope.btnPing === "btn btn-primary active" ? "btn btn-default": "btn btn-primary active";
        $scope.addPing = $scope.addPing === true ? false: true;

        // default form values
        $scope.ping.packetsSent = 1;
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
      console.log(data);

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
