/*
 * Routes and Views to Render
 * public/js/
 * appRoutes.js
 */

angular.module('appRoutes', []).config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {

  $routeProvider.
    when('/', {
      templateUrl: 'views/slice.html',
      controller: 'SliceController'
    }).
    when('/nodes', {
      templateUrl: 'views/node.html',
      controller: 'NodeController'
    }).
    when('/services', {
      templateUrl: 'views/service.html',
      controller: 'ServiceController'
    }).
    when('/blipp', {
      templateUrl: 'views/blipp.html',
      controller: 'BlippController'
    }).
    when('/helm', {
      templateUrl: 'views/helm.html',
      controller: 'HelmController'
    }).
    when('/measurements', {
      templateUrl: 'views/measurement.html',
      controller: 'MeasurementController'
    }).
    when('/help', {
      templateUrl: 'views/help.html',
      controller: 'HelpController'
    }).
    otherwise({redirectTo: '/'});

  $locationProvider.html5Mode(true);

}]);
