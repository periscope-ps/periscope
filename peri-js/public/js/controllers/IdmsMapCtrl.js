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
				initNodes : function(arr){
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
					var tip = d3.tip().attr('class', 'd3-tip').html(function() {
						var x = d3.select(this);
						return x.attr('name') + (x.attr('status')?"<br>Status : " + x.attr('status') : "");						
					});
					svg.call(tip);					
					svg.selectAll('circle.idmsNode')					  					
					  .on('mouseover', tip.show)
					  .on('mouseout', tip.hide);
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
						.attr("transform", function() {return "translate(" + projection(latLongPair) + ")";});
					nodeLocationMap[name] = node ;
					return  node ;
				},			
				setNodeColor: function(name , color){
					nodeLocationMap[name].attr('fill',color);
				},
				/**
				 * 0 for 'on' , 1 for 'off' and '2 and greater' for 'don't know'
				 */
				setStatus : function(name , sCode) {
					var color , status ;
					switch(scode){
					case 0 : status = 'ON' ; color = 'green'; 
					break;
					case 1 : status = 'OFF' ; color = 'red';
					break;
					default : status = 'Unknown' ; color = 'yellow';
					}
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
angular.module('IdmsMapCtrl', []).controller('IdmsMapController', function($scope,Socket,Idms) {
	DownloadMap.init();
	Socket.emit("idms_map",{});
	Socket.on("idms_mapData",function(data){
		console.log("Socket data ",data.data);
		// Use this data to create nodes 
		DownloadMap.initNodes(data.data);		
	});
	
	Socket.on("idms_statusChange",function(data){
		console.log("Node Status changed ");
	});
}); // end controller

