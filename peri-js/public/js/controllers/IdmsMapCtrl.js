/*
 * Idms map Controller
 * public/js/controllers/
 * IdmsMapCtrl.js
 */

function movingLineFromPointToPoint(st , end) {
	return d3.selectAll('svg').append('line')
		.style({stroke:'rgb(255,0,0)', strokeWidth:2})
		.attr('x1',st.x).attr('y1',st.y)
		.attr('x2',st.x).attr('y2',st.y)
		.transition().duration(1000)
		.attr('x2',end.x).attr('y2',end.y)
		;
};
var DownloadMap = (function(){
	// All config 
	var width = 960,height = 500 , selector = '#downloadMap';
	var progressStart = 0 , nodeLocationMap = {};
	var knownLocations = {
			'bloomington' : [-86.526386,39.165325] 
	}
	// The main variables
	var svg , projection , g , path , zoom;
	function clicked(d) {
		  var centroid = path.centroid(d),
		      translate = projection.translate();

		  projection.translate([
		    translate[0] - centroid[0] + width / 2,
		    translate[1] - centroid[1] + height / 2
		  ]);

		  zoom.translate(projection.translate());

		  g.selectAll("path").transition()
		      .duration(700)
		      .attr("d", path);
	}

	function zoomed() {
	  projection.translate(d3.event.translate).scale(d3.event.scale);
	  g.selectAll("path").attr("d", path);
	}	
	var tip ;
	var locationMap = [];
	// The main obj
	var d = {
				init : function(){
					progressStart = 0;
					projection = d3.geo.albersUsa()
					    .scale(1070)
					    .translate([width / 2, height / 2]);
	
					path = d3.geo.path()
					    .projection(projection);
	
					/*
					zoom = d3.behavior.zoom()
					    .translate(projection.translate())
					    .scale(projection.scale())
					    .scaleExtent([height, 8 * height])
					    //.on("zoom", zoomed);*/
	
					svg = d3.select(selector).append("svg")
					    .attr("width", width)
					    .attr("height", height);
	
					g = svg.append("g");
					//.call(zoom);
	
					g.append("rect")
					    .attr("class", "background")
					    .attr("width", width)
					    .attr("height", height);
	
					d3.json("/maps/us.json", function(error, us) {
					  g.append("g")
					      .attr("id", "states")
					    .selectAll("path")
					      .data(topojson.feature(us, us.objects.states).features)
					    .enter().append("path")
					      .attr("d", path)
					      //.on("click", clicked);
	
					  g.append("path")
					      .datum(topojson.mesh(us, us.objects.states, function(a, b) { return a !== b; }))
					      .attr("id", "state-borders")
					      .attr("d", path);
					  //d.initProgessBox();
					  //d._doProgress(loc,5);
					});
				}, 
				initNodes : function(arr,id){
					var color ;
					for(var i=0 ; i < arr.length ; i++ ){
						if(arr[i]){
							switch(arr[i].status){
							case 'ON' :color = 'rgb(0,255,0)';
							break;
							case 'OFF' :color = 'rgb(255,0,0)';
							break;
							// Grey
							default : color = 'yellow' , arr[i].status = 'Unknown';							
							}
							
							d._addLocation(''+arr[i].ip, arr[i].loc , color)
							 .attr('status',arr[i].status);						
						}
					}
					d.initTip();
					d.highlightNode(id);
				},
				initProgessBox : function(){
					svg.append("rect")
				    .attr("class", "background")
				    .attr("width", 30)
				    .attr("height", 300)
				    .style('fill','gray')
				    .attr('x', width - 50)
				    .attr('y', '200')
				    ;
				},	
				highlightNode : function(name){
					var x = nodeLocationMap[name];
					console.log(name);
					if(x){
						// Highlight it						
						console.log(x);
					}
				},
				_doProgress : function(loc,progress){					
					d._moveLineToProgress(loc.attr('location').split(","),loc.attr('color') , progress);					
				},
				doProgress : function(ip , progress){
					var loc =  nodeLocationMap[ip];
					d._moveLineToProgress(loc.attr('location').split(","),loc.attr('color') , progress);
				},
				addKnownLocation : function(name){
					var loc = knownLocations[name];
					if(loc)
						return d._addLocation(name,loc);
					else 
						throw "NoSuchLocation";
				},
				initTip : function(){
					// Add tooltips 
					tip = d3.tip().attr('class', 'd3-tip').html(function() {
						var x = d3.select(this);
						return x.attr('name') + (x.attr('status')?"<br>Status : " + x.attr('status') : "");						
					});
					svg.call(tip);
					var timer ;
					svg.selectAll('circle.idmsNode')					  					
					  .on('mouseover', function(){
						  clearTimeout(timer);
						  tip.show.apply(this,arguments);
					  })
					  .on('mouseout', function(){
						 timer = setTimeout(tip.hide,2000);
					  });
				},
				_addLocation : function(name, latLongPair,color) {		
					var color = color || d.getRandomColor();			
					var node = svg.append("circle")
						.attr("r",5)
						.attr('fill',color)
						.attr('color',color)
						.attr('class',name+" idmsNode")
						.attr('name',name)
						.attr('location',latLongPair)						
						.attr("transform", function() {							
							var loc = projection((latLongPair? latLongPair:[0,0]));
							// Store the hashed location in the map so as to provide a random deviation if  locations overlap
							var hash = Math.floor(loc[0] || 0)+":"+Math.floor(loc[1] || 0);
							if(locationMap[hash]){
								// Give a deviation
								var x ;
								var dev = (x = (Math.random() * 2 - 1)) > 0 ? 5 : -5;
								loc[0] += dev ;
								loc[1] += dev ;
								locationMap[hash]++ ;
							} else {
								locationMap[hash] = 1;
							}							
							return "translate(" + loc + ")";
						});
					nodeLocationMap[name] = node ;
					return  node ;
				},		
				changeStatus : function(changedMap){
					var changed = changedMap || {};
					for(var i in changed){
						console.log('Changing name ', i , changed[i].status);
						d.setStatus(i,changed[i].status);
					}
				},
				setNodeColor: function(name , color){
					nodeLocationMap[name].attr('fill',color);
				},
				/**
				 * 0 for 'on' , 1 for 'off' and '2 and greater' for 'don't know'
				 */
				setStatus : function(name , scode) {
					var color , status ;
					scode =  scode || '';
					switch(scode){
					case 'ON' : status = 'ON' ; color = 'green'; 
					break;
					case 'OFF': status = 'OFF' ; color = 'red';
					break;
					default : status = 'Unknown' ; color = 'yellow';
					}
					if(nodeLocationMap[name])
						nodeLocationMap[name].attr('fill',color).attr('status',status);
				},
				removeLocation : function(name){
					svg.select('circle'+'#'+name).remove();
				},
				_moveLineToProgress : function(loc,color , progress){
					// The progress in percentage 			
					progressStart = progressStart || 0 ; 
					if (progressStart >= 100)
						return;
					if(progressStart + progress >= 100){
						progress = 100 - progressStart ;
					}
					var ratio = 300 / 100 ;									
					// draw bar 
					var prog = [width - 50 , 200 + (progressStart*ratio)];
					var h = ratio * progress , w = 30 ; 				
					d._move(projection(loc), prog , color)
					.each("end", function(){						
						svg.append('rect')
						.attr("fill", color)
						.attr("width", w)
				    	.attr("height", h)
				    	.attr('x', width - 50)
				    	.attr('y', 200 + (progressStart*ratio));
						progressStart += progress ;
					}).transition().duration(500).remove();
				},
				getRandomColor : function(){
					var r = function(){return Math.floor(Math.random() * 255);};
					return 'rgb('+r()+','+r()+','+r()+')';
				},
				_move : function (st , end , color ) {
					var y2 = end[1];
					return d3.selectAll('svg').append('line')
						.style({stroke: color , strokeWidth:2})
						.attr('x1',st[0]).attr('y1',st[1])
						.attr('x2',st[0]).attr('y2',st[1])
						.transition().duration(500)
						.attr('x2',end[0]).attr('y2',y2)
						//.transition().duration(500).remove()
						;					
				}
	};
	d.nodeLocationMap = nodeLocationMap;
	return d;
})();
angular.module('IdmsMapCtrl', []).controller('IdmsMapController', function($rootScope,$scope,$routeParams,Socket,Idms) {
	DownloadMap.init();
	var id = $routeParams.id ;	
	 var getAccessIp = function(x){
		  return ((x.accessPoint || "").split("://")[1] || "").split(":")[0] || ""; 
	    };
	console.log('scope services ',$scope.services);
	function initNodes(services){
		// Use the services which have a location 
		var immediateLoc = [];
		var getLoc = [];
		for (var i = 0 ; i < services.length ; i++){
			var k = services[i];
			// TODO check if this location is the right field
			if(k.location)
				immediateLoc.push(k);
			else 
				getLoc.push(k);
		};
		
		//Run initNodes for immediateLoc 
		DownloadMap.initNodes(immediateLoc,id);
		// Now get location from service and then init it
		var ipArr = getLoc.map(function(x){
			return getAccessIp(x); 
		});
		Socket.emit("idms_map",{ipArr : ipArr});
		Socket.on("idms_mapData",function(dta){
			console.log("Socket data ",dta.data);
			var map = dta.data;
			var data = getLoc;
			
			for(var i=0 ; i < data.length ; i++){
				var val = data[i];
				val.ip = getAccessIp(val);
				val.loc = map[val.ip];
			}
			console.log("Socket data ",data);
			// Use this data to create nodes 
			DownloadMap.initNodes(data,id);
		});
	}
	if($rootScope.idmsServices){
		services = $rootScope.idmsServices;
		initNodes(services);
	} else {
		Idms.getServices(function(services) {
			
			// Need this services for the map as well -- Yes i am pollution the global scope , will find a better way later 
		    $rootScope.idmsServices = $scope.services = $scope.services || $rootScope.idmsServices || [];

		    if (typeof services =='string')
		      services = JSON.parse(services);

		    $rootScope.idmsServices  = $scope.services = $scope.services.concat(services);
		    // Now initNodes 
		    services = $rootScope.idmsServices;
		    console.log('recieved se ',services);
			initNodes(services);
		});
	};
	window.k = $rootScope ;
	$rootScope.$watchCollection('idmsServices',function(services , old){
		if(!services || !old) return ;		
		console.log('checking for change ', services , old);
		// Set the color here according to service status 
		// Find if status has changed and modify the ones that have
		// Convert them into map based on there ip 
		var newMap = {} , oldMap = {};		
		for (var i=0 ; i < services.length ; i++){
			var k = services[i];
			newMap[getAccessIp(k)] = k;			
		}
		/*
		for (var i=0 ; i < old.length ; i++){
			var k = old[i];
			oldMap[getAccessIp(k)] = k;			
		}
		var changed = {};		
		// Now compare 
		for(var i in newMap) {
			var it = newMap[i];
			var ot = oldMap[i];			
			if(ot && ot.status && it.status != ot.status ){
				// Then add to changed
				console.log('changed' , i);
				changed[i] = it.status;
			}
		}*/
		// send the changedMap to DownloadMap
		DownloadMap.changeStatus(newMap);
	},true);
	
	
	Socket.on("idms_statusChange",function(data){
		console.log("Node Status changed ");
	});
}); // end controller

