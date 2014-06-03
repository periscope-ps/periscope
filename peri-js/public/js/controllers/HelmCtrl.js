/*
 * Helm Page Controller
 * public/js/controllers/
 * HelmCtrl.js
 */

angular.module('HelmCtrl', []).controller('HelmController', function($scope, $http) {

  $http.get('/api/nodes')
    .success(function(data) {

      $scope.helmData = {};
      $scope.alerts = [];

      $scope.addAlert = function(msg, type) {
        $scope.alerts.push({type: type, msg: msg});
      };
      $scope.closeAlert = function(index) {
        $scope.alerts.splice(index, 1);
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

          /*angular.forEach($scope.nodes,function(value,index){
            "name":value.name;
          })*/

          var helm_measurement = {
            "vnodes": {
              "domain_ion.internet2.edu_node_rtr.seat": "52:e4:00:3c:13:44",
              "domain_ion.internet2.edu_node_rtr.salt": "a3:54:00:00:b7:5b",
              "domain_ion.internet2.edu_node_rtr.losa": "64:e3:87:90:ff:e2"
            },
            "probes":{
              "iperf":{
                "probe_defaults":{
                  "collection_schedule":"adaptive.silent_lamb",
                    "schedule_params": {"every": $scope.helm.every, "duration":$scope.helm.duration, "num_to_schedule":$scope.helm.num},
                    "reporting_params": $scope.helm.report,
                    "collection_size":$scope.helm.size,
                    "collection_ttl":$scope.helm.ttl,
                    "ms_url": "http://localhost:8888",
                    "name":$scope.helm.desc
                }
              }
            }
          };

          $http({
            method: 'POST',
            url: '/api/helm',
            data: helm_measurement,
            headers: {'Content-type': 'application/perfsonar+json'}
          }).
          success(function(data, status, headers, config) {
            // $scope.addAlert(data, 'success');
            // $scope.addAlert(status, 'success');
            // $scope.addAlert(headers, 'success');
            // $scope.addAlert(config, 'success');
            var measurement = data;
            $scope.addAlert('HELM Test: ' + measurement.configuration.name + ' submitted to UNIS', 'success');
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
      $scope.helmReset();
      $scope.helmUnchanged = function(helm) {
        return angular.equals(helm, $scope.helmData);
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
