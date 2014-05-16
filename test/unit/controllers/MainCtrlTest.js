/*
 * Home Page Controller Test
 * test/unit/controllers/
 * MainCtrlTest.js
 */

describe('Unit: MainController', function() {
  // load the app module that the controller belongs to
  beforeEach(module('measurementApp'));

  var ctrl, scope;  // mock controller and scope

  // inject controller and root scope services
  beforeEach(inject(function($controller, $rootScope) {
    // create scope that is child of $rootScope
    scope = $rootScope.$new();

    // create a controller
    ctrl = $controller('MainController', {
      $scope: scope,
    });
  }));

  /* tests begin below */

  it('should have defined MainController', function() {
    expect(ctrl).toBeDefined();
  });

  // create mock slice data then test against mock data

  /*it('should have $scope.gn = "pcvm2-2.geni.kettering.edu"', function() {
    expect(scope.gn).toEqual("pcvm2-2.geni.kettering.edu");
  });*/

})
