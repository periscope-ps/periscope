include('/static_media/js/raphael/raphael-min.js');
include('/static_media/js/raphael/dracula_graph.js');
include('/static_media/js/raphael/dracula_graffle.js');

function pointsOnCircle(center, radius, n) {
    var points = [];
    var alpha = Math.PI * 2 / n;
    
    for (var m = 0; m < n; m++) {
	var theta = alpha * m;
	points[m] = [center[0] + Math.cos(theta)*radius,
		     center[1] + Math.sin(theta)*radius];
    }
    return points;
};

function closestPoints(source_points, sink_points) {
    var m_dist = 0;
    var m_index = [];
    for (var j = 0; j < source_points.length; j++) {
	for (var k = 0; k < sink_points.length; k++) {
	    
	    d = Math.sqrt(Math.pow(sink_points[j][0] - source_points[k][0], 2) +
			  Math.pow(sink_points[j][1] - source_points[k][1], 2));
	    
	    if (m_dist==0) {
		m_dist = d;
		m_index = [j, k];
	    }
	    else {
		if (d > m_dist) {
		    m_dist = d;
		    m_index = [j, k];
		}
	    }
	}
    }
    return m_index;
};

function rand (n) {
    return ( Math.floor ( Math.random ( ) * n + 1 ) );
}

function doSpring(items, request) {
    
    function translate(point, minX, minY, fX, fY, rad) {
        return [
		Math.round((point[0] - minX) * fX + rad),
		Math.round((point[1] - minY) * fY + rad)
		];
    };

    var node_ports = [];
    var positioned = [];
    var g = new Graph();

    // add all the nodes to the graph
    for(i = 0; i < items.length; i++) {
	var shapeItem = items[i];
	var shapeId = topoStore.getValue(shapeItem, 'id', '');
	var shapeName = topoStore.getValue(shapeItem, 'name', '');
	g.addNode(shapeId, {label: shapeName});

	node_ports[shapeId] = [];
    }

    // find links and add edges to nodes in graph
    // this is all based on shape ids, not the objects!
    function addEdges(items) {
	for (i = 0; i < items.length; i++) {
	    var sourceID = items[i].source[0].parent[0].id[0];
	    var sinkID = items[i].sink[0].parent[0].id[0];

	    if (!(sourceID && sinkID))
		    continue;

	    g.addEdge(sourceID, sinkID);
	}
    };
    topoStore.fetch({
	    query: { type: "link" },
		onComplete: addEdges
		});
    
    // do the auto-layout
    var layouter = new Graph.Layout.Spring(g);
    layouter.layout();

    var s_dim = surface.getDimensions();
    var radius = 60;

    // now update the topo store with the new node positions
    for (i = 0; i < items.length; i++) {
	var shapeItem = items[i];
        var shapeId = topoStore.getValue(shapeItem, 'id', '');
	
	var factorX = (s_dim.width - 2 * radius) / (g.layoutMaxX - g.layoutMinX);
	var factorY = (s_dim.height - 2 * radius) / (g.layoutMaxY - g.layoutMinY);
	
	var point = translate([g.nodes[shapeId].layoutPosX, g.nodes[shapeId].layoutPosY],
			      g.layoutMinX,
			      g.layoutMinY,
			      factorX,
			      factorY,
			      radius);
	
	topoStore.setValue(shapeItem, 'x', point[0]);
	topoStore.setValue(shapeItem, 'y', point[1]);
    }
    
    // update all the port-pair positions
    function updateLinkPorts(items, request) {
	for (var i = 0; i < items.length; i++) {
	    var shapeItem = items[i];
	    
	    var sourcePort = shapeItem.source[0];
            var sinkPort = shapeItem.sink[0];
	    
	    var sourceNode = sourcePort.parent[0];
	    var sinkNode = sinkPort.parent[0];
	    
	    var sourcePoint = [topoStore.getValue(sourceNode, 'x', ''),
			       topoStore.getValue(sourceNode, 'y', '')
			       ];
	    var sinkPoint = [topoStore.getValue(sinkNode, 'x', ''),
			     topoStore.getValue(sinkNode, 'y', '')
			     ];

	    var sourceWidth =  sourceNode.width[0];
            var sinkWidth = sinkNode.width[0];

	    // let's get 20 points around each node...
	    var source_points = pointsOnCircle(sourcePoint, sourceWidth, 20);
	    var sink_points = pointsOnCircle(sinkPoint, sinkWidth, 20);
	    
	    // now find the closest points for the link
	    var m_points = closestPoints(source_points, sink_points);

	    topoStore.setValue(sourcePort, 'x', source_points[m_points[0]][0]);
	    topoStore.setValue(sourcePort, 'y', source_points[m_points[0]][1]);
	    topoStore.setValue(sinkPort, 'x', sink_points[m_points[1]][0]);
            topoStore.setValue(sinkPort, 'y', sink_points[m_points[1]][1]);
	    
	    node_ports[topoStore.getValue(sourceNode, 'id', '')][m_points[0]] = 1;
	    node_ports[topoStore.getValue(sinkNode, 'id', '')][m_points[1]] = 1;

	    positioned[topoStore.getValue(sourcePort, 'id', '')] = 1;
	    positioned[topoStore.getValue(sinkPort, 'id', '')] = 1;
	}
    };
    topoStore.fetch({
            query: { type: "link" },
                onComplete: updateLinkPorts
                });
    
    // update the lonely ports
    function updatePorts(items, request) {
	for (var i = 0; i < items.length; i++) {
	    var sPort = items[i];
	    
	    if (positioned[topoStore.getValue(sPort, 'id', '')] == 1)
		continue;
	    
	    sNode = sPort.parent[0];
	    sPoint = [topoStore.getValue(sNode, 'x', ''),
		      topoStore.getValue(sNode, 'y', '')
		      ];
	    s_points = pointsOnCircle(sPoint, 30, 20);

	    sNodeID = topoStore.getValue(sNode, 'id', '');
	    var p_used = node_ports[sNodeID];
	    for (var j = 0; j < p_used.length; j++) {
		if (p_used[j] != 1) {
		    topoStore.setValue(sPort, 'x', s_points[j][0]);
		    topoStore.setValue(sPort, 'y', s_points[j][1]);
		    node_ports[sNodeID][j] = 1;
		    break;
		}
	    }
	    positioned[topoStore.getValue(sPort, 'id', '')] = 1;
	}
    }
    topoStore.fetch({
            query: { type: "port" },
                onComplete: updatePorts
                });


    var renderer = new Graph.Renderer.Raphael('canvas', g, 1000, 400);
    renderer.draw();
 
    redraw = function() {
        layouter.layout();
        renderer.draw();
    };    
};
