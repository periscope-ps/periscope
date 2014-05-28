/*
 * Blipp Page Controller
 * public/js/controllers/
 * BlippCtrl.js
 */

angular.module('BlippCtrl', []).controller('BlippController', function($scope, $http) {

  $http.get('/nodes')
    .success(function(data) {

      $scope.pingData = {};
      $scope.timeTypes = [
        {type:'Seconds'},
        {type:'Minutes'},
        {type:'Hours'},
        {type:'Days'}
      ];

      $scope.pingSubmit = function(ping) {

        if (ping.$invalid) {
          // If form is invalid, return and let AngularJS show validation errors.
          $scope.submitDanger = true;
          $scope.messages = 'Invalid form submitted.';
          return;
        } else {
          // Trigger success flag
          $scope.submitSuccess = true;
          $scope.messages = 'Success, have a beer!';

          $scope.pingData = angular.copy(ping);

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
