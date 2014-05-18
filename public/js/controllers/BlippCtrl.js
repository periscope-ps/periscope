/*
 * Blipp Page Controller
 * public/js/controllers/
 * BlippCtrl.js
 */

angular.module('BlippCtrl', []).controller('BlippController', function($scope, $http) {

  $http.get('/nodes')
    .success(function(data) {

      $scope.togglePing = function() {
        $scope.btnPing = $scope.btnPing === "btn btn-primary active" ? "btn btn-default": "btn btn-primary active";
        $scope.addPing = $scope.addPing === true ? false: true;
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
