/*
 * Rest Services for a Service
 * public/js/services/
 * ServiceService.js
 */

angular.module('ServiceService', []).service('Service', function($http, Socket) {
	
  this.getServices = function(services , start , end , opt) {
	// Limiting the size here .... Default to 10
	var start = start || 0 ;
	var end = end || 10 ;
	var skip = start ; 
	var limit = end - start ;
	limit =  limit > 0 ? limit : 10;	
	opt = opt || {};
	var paramStr = "&"+$.param(opt.f || {});	
	var sortStr = opt.sort ? "&sort="+opt.sort : ""; 
    $http.get('/api/services?limit='+limit+"&skip="+skip+paramStr + sortStr).success(function(data,status , headers) {
      console.log('HTTP Service Request: ' , data);      
      var count = parseInt(headers("unis_x-count"))
      services(data,count);

      Socket.on('service_data',function(data){
        console.log('Incoming Socket Service Data: ' , data);
        services(data);
      });
    }).error(function(data) {
      console.log('HTTP Service Error: ' ,  data);
    });
  };
});
