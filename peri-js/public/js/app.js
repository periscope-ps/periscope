/*
 * Setup Our Angular App
 * public/js/
 * app.js
 */

angular.module('measurementApp', [ 'ngRoute', 'ngAnimate', 'ui.utils',
		'ui.bootstrap', 'nvd3ChartDirectives', 'directedGraphModule',
		'appRoutes', 'SliceCtrl', 'SliceService', 'NodeCtrl', 'NodeService',
		'ServiceCtrl', 'ServiceService', 'MeasurementCtrl', 'MeasurementService',
		'MetadataCtrl', 'MetadataService', 'IdmsMapCtrl', 'IdmsCtrl', 'IdmsService',
    'PortService', 'SocketService']
    ).run(function($rootScope, $http, $q, $timeout, $location, Socket,$route) {
    var smPromises = [] ;

    $rootScope.getServices = function(cb){
      smPromises.push(cb);
    };

    $http.get('/api/services').success(function(data) {
      console.log('HTTP Service Request: ' , data);
      console.log(data.length);

      var uniqueServices = [];
      var services = [];

      for(var i = 0; i < data.length; i++) {
        if(uniqueServices.indexOf(data[i].id) == -1) {
          uniqueServices.push(data[i].id);
        }
      }

      console.log(uniqueServices.length);
      console.log(uniqueServices);

      getServices = function() {
        var promises = [];

        for(var i = 0; i < uniqueServices.length; i++) {
          promises.push($http.get('/api/services/' + uniqueServices[i]).success(function(data) {
            services.push(data);
          }));
        }

        return $q.all(promises);
      };

      getServices().then(function(data) {
        for(var i = 0 ; i < smPromises.length ; i++){
          try{
            smPromises[i](services);
          }catch(e){}

        };

        // set timer value
        onTimeout = function() {
          for(var i = 0; i < services.length; i++) {

            if(services[i].ttl == 0) {
              services[i].status = 'Unknown';
            } else if(services[i].ttl < 0) {
              services[i].status = 'OFF';
            } else {
              services[i].ttl--;
            }
          }
          //continue timer
          timeout = $timeout(onTimeout, 1000);
        }

        $rootScope.services = services;

        // set ttl value
        for(var i = 0; i < services.length; i++) {
          var now = Math.round(new Date().getTime() / 1e3) //seconds
          services[i].ttl = Math.round(((services[i].ttl + (services[i].ts / 1e6)) - now));
        }

        // start timer
        var timeout = $timeout(onTimeout, 1000);

        // open sockets
        Socket.emit('service_request', {});
      });
    });

    $http.get('/api/ports').success(function(data) {
      console.log('Port Request: ' + data);

      Socket.emit('port_request', {});

      $rootScope.ports = data;
    }).error(function(data) {
      console.log('Port Error: ' + data);
    });

    $http.get('/api/nodes').success(function(data) {
      console.log('Node Request: ' + data);

      Socket.emit('node_request', {});

      $rootScope.nodes = data;
    }).error(function(data) {
      console.log('Node Error: ' + data);
    });

    $http.get('/api/measurements').success(function(data) {
      console.log('Measurement Request: ' + data);

      Socket.emit('measurement_request', {});


      $rootScope.measurements = data;
    }).error(function(data) {
      console.log('Measurement Error: ' + data);
    });

    $http.get('/api/metadata').success(function(data) {
      console.log('Metadata Request: ' + data);

      Socket.emit('metadata_request', {});

      $rootScope.metadata = data;
    }).error(function(data) {
      console.log('Metadata Error: ' + data);
    });
  });


