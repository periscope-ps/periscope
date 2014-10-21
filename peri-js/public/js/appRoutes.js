/*
 * Routes and Views to Render
 * public/js/
 * appRoutes.js
 */

angular.module('appRoutes', []).config(['$routeProvider', '$locationProvider', 'cfpLoadingBarProvider', function($routeProvider, $locationProvider, cfpLoadingBarProvider) {

  cfpLoadingBarProvider.includeSpinner = false;

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
    when('/measurements', {
      templateUrl: 'views/measurements.html',
      controller: 'MeasurementController'
    }).
    when('/measurements/:id', {
      templateUrl: 'views/measurement.html',
      controller: 'MeasurementController'
    }).
    when('/metadata', {
      templateUrl: 'views/metadatas.html',
      controller: 'MetadataController'
    }).
    when('/metadata/:id', {
      templateUrl: 'views/metadata.html',
      controller: 'MetadataController'
    }).
    when('/idms', {
      templateUrl: 'views/idms.html',
      controller: 'IdmsController'
    }).
    when('/idms/:id', {
      templateUrl: 'views/idms_data.html',
      controller: 'IdmsController'
    }).
    when('/idmsMap', {
        templateUrl: 'views/idmsMap.html',
        controller: 'IdmsMapController'
    }).
    when('/idmsMap/:id', {
        templateUrl: 'views/idmsMap.html',
        controller: 'IdmsMapController'
    }).
    otherwise({redirectTo: '/'});

  $locationProvider.html5Mode(true);

}]);
