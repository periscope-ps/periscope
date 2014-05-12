/*
 * Routes and Views to Render
 * public/js/
 * appRoutes.js
 */

angular.module('appRoutes', []).config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {

  $routeProvider

    .when('/', {
      templateUrl: 'views/home.html',
      controller: 'MainController'
    })

    .when('/nodes', {
      templateUrl: 'views/node.html',
      controller: 'NodeController'
    })

    .when('/services', {
      templateUrl: 'views/service.html',
      controller: 'ServiceController'  
    });

  $locationProvider.html5Mode(true);

}]);