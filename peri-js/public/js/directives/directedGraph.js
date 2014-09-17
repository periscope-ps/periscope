/*
 * Custom HTML Directives
 * public/js/
 * directives.js
 */
(function(){
	function resetMouseVars() {
		mousedown_node = null;
		mouseup_node = null;
		mousedown_link = null;
		
		scope.g_links = links.map(function(x){
			return [x.source.id,x.target.id];
		});
	}
	
	// update force layout (called automatically each iteration)
	function tick() {
		// draw directed edges with proper padding from node centers
		path.attr('d', function(d) {
			var deltaX = d.target.x - d.source.x,
			deltaY = d.target.y - d.source.y,
			dist = Math.sqrt(deltaX * deltaX + deltaY * deltaY),
			normX = deltaX / dist,
			normY = deltaY / dist,
			sourcePadding = d.left ? 17 : 12,
					targetPadding = d.right ? 17 : 12,
							sourceX = d.source.x + (sourcePadding * normX),
							sourceY = d.source.y + (sourcePadding * normY),
							targetX = d.target.x - (targetPadding * normX),
							targetY = d.target.y - (targetPadding * normY);
			return 'M' + sourceX + ',' + sourceY + 'L' + targetX + ',' + targetY;
		});
		
		circle.attr('transform', function(d) {
			return 'translate(' + d.x + ',' + d.y + ')';
		});
	}
	
	// update graph (called when needed)
	function restart() {
		// path (link) group
		path = path.data(links);
		
		// update existing links
		path.classed('selected', function(d) { return d === selected_link; })
		.style('marker-end', function(d) { return 'url('+curUrl+'#end-arrow)'; });
		
		// add new links
		path.enter().append('svg:path')
		.attr('class', 'link')
		.classed('selected', function(d) { return d === selected_link; })
		.style('marker-end', function(d) { return 'url('+curUrl+'#end-arrow)'; })
		.on('mousedown', function(d) {
			if(d3.event.ctrlKey) return;
			
			// select link
			mousedown_link = d;
			console.log("mousedown_link: " + mousedown_link);
			if(mousedown_link === selected_link) selected_link = null;
			else selected_link = mousedown_link;
			selected_node = null;
			restart();
		});
		// remove old links
		path.exit().remove();
		
		// circle (node) group
		// NB: the function arg is crucial here! nodes are known by id, not by index!
		circle = circle.data(nodes, function(d) { return d.id; });
		
		// update existing nodes (reflexive & selected visual states)
		circle.selectAll('circle')
		.style('fill', function(d) { return (d === selected_node) ? d3.rgb(colors(d.id)).brighter().toString() : colors(d.id); })
		.classed('reflexive', function(d) { return d.reflexive; });
		
		// add new nodes
		var g = circle.enter().append('svg:g');
		
		g.append('svg:circle')
		.attr('class', 'node')
		.attr('r', 18)
		.style('fill', function(d) { return (d === selected_node) ? d3.rgb(colors(d.id)).brighter().toString() : colors(d.id); })
		.style('stroke', function(d) { return d3.rgb(colors(d.id)).darker().toString(); })
		.classed('reflexive', function(d) { return d.reflexive; })
		.on('mouseover', function(d) {
			if(!mousedown_node || d === mousedown_node) return;
			// enlarge target node
			d3.select(this).attr('transform', 'scale(1.1)');
		})
		.on('mouseout', function(d) {
			if(!mousedown_node || d === mousedown_node) return;
			// unenlarge target node
			d3.select(this).attr('transform', '');
		})
		.on('mousedown', function(d) {
			if(d3.event.ctrlKey) return;
			
			// select node
			mousedown_node = d;
			if(mousedown_node === selected_node) selected_node = null;
			else selected_node = mousedown_node;
			selected_link = null;
			
			// reposition drag line
			drag_line
			.style('marker-end', 'url(#end-arrow)')
			.classed('hidden', false)
			.attr('d', 'M' + mousedown_node.x + ',' + mousedown_node.y + 'L' + mousedown_node.x + ',' + mousedown_node.y);
			
			restart();
		})
		.on('mouseup', function(d) {
			if(!mousedown_node) return;
			
			// needed by FF
			drag_line
			.classed('hidden', true)
			.style('marker-end', '');
			
			// check for drag-to-self
			mouseup_node = d;
			if(mouseup_node === mousedown_node) { resetMouseVars(); return; }
			
			// unenlarge target node
			d3.select(this).attr('transform', '');
			
			// add link to graph (update if exists)
			// NB: links are strictly source < target; arrows separately specified by booleans
			var source, target, link;
			if(mousedown_node.id < mouseup_node.id) {
				console.log("< mousedown_node.id: " + mousedown_node.id);
				console.log("< mouseup_node.id: " + mouseup_node.id);
				source = mousedown_node;
				target = mouseup_node;
				console.log("< source: " + source.id);
				console.log("< target: " + target.id);
				link = {source: source, target: target};
				links.push(link);
			} else {
				console.log("> mousedown_node.id: " + mousedown_node.id);
				console.log("> mouseup_node.id: " + mouseup_node.id);
				source = mousedown_node;
				target = mouseup_node;
				console.log("> source: " + source.id);
				console.log("> target: " + target.id);
				link = {source: source, target: target};
				links.push(link);
			}
			
			// select new link
			selected_link = link;
			selected_node = null;
			restart();
		}).on('blur',function(){
			selected_node = null ;
		});
		
		// show node IDs
		g.append('svg:text')
		.attr('x', 0)
		.attr('y', 4)
		.attr('class', 'id')
		.text(function(d) { return d.id; });
		
		// remove old nodes
		circle.exit().remove();
		
		// set the graph in motion
		force.start();
	}
	
	function mousedown() {
		// prevent I-bar on drag
		// d3.event.preventDefault();
		
		// because :active only works in WebKit?
		svg.classed('active', true);
		
		if(d3.event.ctrlKey || mousedown_node || mousedown_link) return;
		
		restart();
	}
	
	function mousemove() {
		if(!mousedown_node) return;
		
		// update drag line
		drag_line.attr('d', 'M' + mousedown_node.x + ',' + mousedown_node.y + 'L' + d3.mouse(this)[0] + ',' + d3.mouse(this)[1]);
		
		restart();
	}
	
	function mouseup() {
		if(mousedown_node) {
			// hide drag line
			drag_line
			.classed('hidden', true)
			.style('marker-end', '');
		}
		
		// because :active only works in WebKit?
		svg.classed('active', false);
		
		// clear mouse event vars
		resetMouseVars();
	}
	// only respond once per keydown
	var lastKeyDown = -1;
	function keydown() {			
		if(!selected_node && !selected_link) return;
		
		d3.event.preventDefault();		
		if(lastKeyDown !== -1) return;
		lastKeyDown = d3.event.keyCode;
		
		switch(d3.event.keyCode) {
		case 8: // backspace
		case 46: // delete
			if(selected_link) {
				links.splice(links.indexOf(selected_link), 1);
			}
			selected_link = null;
			selected_node = null;
			resetMouseVars();
			restart();
			break;
		}
	}
	
	function keyup() {
		lastKeyDown = -1;		
	}
	
	// vars required 
	
	var nodes = [], links = []  , width , height , force,drag_line,scope,curUrl;
	var path;
	var selected_node = null,
	selected_link = null,
	mousedown_link = null,
	mousedown_node = null,
	mouseup_node = null , oldSelected_node , oldSelected_link;
	
	angular.module('directedGraphModule', []).directive('directedGraph', function(Node,$location) {
		return {
			restrict: 'E',
			replace: true,
			template: '<div id="graphSelect"></div>',
			scope: { // attributes bound to the scope of the directive
				g_nodes: '=nodes',
				g_links: '=links'
			},
			link: function (scpe, element, attrs) {
				
				d3.select('#graphSelect').on('mouseout' , function(){ 				
					oldSelected_node = selected_node;
					oldSelected_link = selected_link;
					selected_node = null,
					selected_link = null;
				}).on('mouseover',function(){
					if(oldSelected_node)
						selected_node = oldSelected_node;
					if(oldSelected_link)
						selected_link = oldSelected_link;
					oldSelected_link = oldSelected_node = null;
				});
				
				scope = scpe ;
				nodes = [], links = [];
				// set up SVG for D3
				width  = 600,
				height = 400,
				colors = d3.scale.category10();
				curUrl = $location.$$url;
				svg = d3.select('#graphSelect')
				.append('svg')
				.attr('width', width)
				.attr('height', height);
				var i = 0;
				var flag = true ;
				Node.getNodes(function(http_nodes) {
					if(!flag)
						return;
					flag = false ;
					console.log("http nodes: " , http_nodes);
					
					// Reuse this function
					svg = d3.select('#graphSelect svg');
					var ndes = [];
					for(var j = 0; j < http_nodes.length; j++ , i++) {
						ndes[j] = {id: i, reflexive: false};
						nodes[i] = {id: i, reflexive: false};
						scope.g_nodes[i] = [i, http_nodes[j].name, http_nodes[j].id];						
					}
					
					// init D3 force layout
					force = d3.layout.force()
					.nodes(nodes)
					.links(links)
					.size([width, height])
					.linkDistance(150)
					.charge(-500)
					.on('tick', tick);
					
					// define arrow markers for graph links
					svg.append('svg:defs').append('svg:marker')
					.attr('id', 'end-arrow')
					.attr('viewBox', '0 -5 10 10')
					.attr('refX', 6)
					.attr('markerWidth', 4)
					.attr('markerHeight', 4)
					.attr('orient', 'auto')
					.append('svg:path')
					.attr('d', 'M0,-5L10,0L0,5')
					.attr('fill', '#000');
					
					svg.append('svg:defs').append('svg:marker')
					.attr('id', 'start-arrow')
					.attr('viewBox', '0 -5 10 10')
					.attr('refX', 4)
					.attr('markerWidth', 4)
					.attr('markerHeight', 4)
					.attr('orient', 'auto')
					.append('svg:path')
					.attr('d', 'M10,-5L0,0L10,5')
					.attr('fill', '#000');
					
					// line displayed when dragging new nodes
					drag_line = svg.append('svg:path')
					.attr('class', 'link dragline hidden')
					.attr('d', 'M0,0L0,0');
					
					// handles to link and node element groups
					path = svg.append('svg:g').selectAll('path'),
					circle = svg.append('svg:g').selectAll('g');
					
					// mouse event vars
					selected_node = null,
					selected_link = null,
					mousedown_link = null,
					mousedown_node = null,
					mouseup_node = null;
					
					// app starts here
					svg.on('mousedown', mousedown)
					.on('mousemove', mousemove)
					.on('mouseup', mouseup);
					d3.select(window)
					.on('keydown', keydown)
					.on('keyup', keyup);
					restart();
					
					// Add tooltips 
					var tip = d3.tip().attr('class', 'd3-tip').html(function(d) { return scope.g_nodes[d.id].slice(1).join("<br/>"); });;
					svg.call(tip);
					svg.selectAll('circle.node')					  					
					  .on('mouseover', tip.show)
					  .on('mouseout', tip.hide);
					 
				});
			}
		};
	});
})();
