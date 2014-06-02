/*
 * Slice Page Controller
 * public/js/controllers/
 * SliceCtrl.js
 */

angular.module('SliceCtrl', []).controller('SliceController', function($scope, Slice) {

  Slice.getSlice(function(sliceInfo) {
    $scope.geniSlice = sliceInfo[0];
  });
});
