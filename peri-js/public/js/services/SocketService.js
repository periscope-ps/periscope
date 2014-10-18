/*
 * Socket Service
 * public/js/services/
 * SocketService.js
 */

angular.module('SocketService', []).service('Socket', function($rootScope, $location) {

  var socket = io.connect($location.absUrl());

  this.on = function (eventName, callback) {
    socket.on(eventName, function () {
      var args = arguments;
      $rootScope.$apply(function () {
        callback.apply(socket, args);
      });
    });
  };
  this.emit = function (eventName, data, callback) {
    socket.emit(eventName, data, function () {
      var args = arguments;
      $rootScope.$apply(function () {
        if (callback) {
          callback.apply(socket, args);
        }
      });
    });
  };

});
