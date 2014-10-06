/*
 * Eodn Page Controller
 * public/js/controllers/
 * EodnCtrl.js
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
					  var loc = d.addKnownLocation('bloomington');					  
						d._moveLineToProgress(loc.attr('location').split(","),loc.attr('color'));
						d.initProgessBox();
					});
					
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
				addKnownLocation : function(name){
					var loc = knownLocations[name];
					if(loc)
						return d._addLocation(name,loc);
					else 
						throw "NoSuchLocation";
				},
				_addLocation : function(name, latLongPair){		
					var color = d.getRandomColor();					
					return svg.append("circle")
						.attr("r",5)
						.attr('fill',color)
						.attr('color',color)
						.attr('class',name)
						.attr('name',name)
						.attr('location',latLongPair)
						.attr("transform", function() {return "translate(" + projection(latLongPair) + ")";});					
				},				
				removeLocation : function(name){
					svg.select('circle'+'#'+name).remove();
				},
				_moveLineToProgress : function(loc,color){										
					var prog = [width - 50 , 200];
					var k = d._move(projection(loc), prog , color);
					//.on('end', function(){				alert(11);			});
				},
				getRandomColor : function(){
					var r = function(){return Math.floor(Math.random() * 255);};
					return 'rgb('+r()+','+r()+','+r()+')';
				},
				_move : function (st , end , color ) {
					return d3.selectAll('svg').append('line')
						.style({stroke: color , strokeWidth:2})
						.attr('x1',st[0]).attr('y1',st[1])
						.attr('x2',st[0]).attr('y2',st[1])
						.transition().duration(1000)
						.attr('x2',end[0]).attr('y2',end[1])
						.transition().duration(100).remove()							
						;					
				}
	};
	return d;
})();
angular.module('EodnCtrl', []).controller('EodnController', function($scope, $http, Service, Slice) {
	DownloadMap.init();
}); // end controller

