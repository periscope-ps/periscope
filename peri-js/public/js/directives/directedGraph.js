/*
 * Custom HTML Directives
 * public/js/
 * directives.js
 */

angular.module('directedGraphModule', []).directive('directedGraph', function() {
    return {
      restrict: 'AE',
      replace: 'true',
      template: '<h3>Hello World!!</h3>'
    };
});
