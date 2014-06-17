/*
 * Metadata Page Controller
 * public/js/controllers/
 * MetadataCtrl.js
 */

angular.module('MetadataCtrl', []).controller('MetadataController', function($scope, Metadata) {

  Metadata.getMetadatas(function(metadatas) {
    $scope.metadatas = metadatas;
  });

});
