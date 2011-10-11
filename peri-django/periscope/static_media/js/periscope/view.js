dojo.require("dojox.gfx");
dojo.require("dojox.gfx.move");
dojo.require("dojox.gfx.fx");
dojo.require("dijit.layout.ContentPane");
dojo.require("dijit._Templated");
dojo.require("dojo.dnd.TimedMoveable");
dojo.require("dojo.colors");
dojo.require("dijit.Tooltip");
dojo.require("dijit.Dialog");
dojo.require("dojox.charting.Chart2D");
dojo.require("dojox.layout.FloatingPane");
dojo.require("periscope.Tooltip");

var pathLinks = {};
var anims = [];
var anims2 = [];
var chunks = [];
var prev_row = -1;
var path_text = null;

function visualizeTransferPath(e) {
    var selectedRow = transferGrid.getItem(e.rowIndex);

    if (!selectedRow) {
	return;
    }
    
    if (prev_row == e.rowIndex) {
        return;
    }
    else {
	prev_row = e.rowIndex;
    }

    var txtOpts = {
	x: 10,
	y: 580,
	align: "right",
	font: "Helvetica",
	size: 16,
	weight: "bold",
	fill: "black",
	bg: "orange",
	text: 'Visualizing Path: ' + selectedRow.src + ':' + selectedRow.sport + '  <--->  ' + 
	    selectedRow.dst + ':' + selectedRow.dport 
    };
    
    path_text = add_surface_text(txtOpts);

    var ind = -1;
    for (var i=0; i<paths.length; i++) {
	if (paths[i].t_id == selectedRow.t_id) {
	    ind = i;
	    break;
	}
    }

    if (ind >= 0) {
	var currp = paths[i];
	var srcNode = idShapeMap[currp.src_id];
	var dstNode = idShapeMap[currp.dst_id];
	
	srcNode.children[0].setFill("orange");
	dstNode.children[0].setFill("orange");
	
	for (var i=0; i<currp.link_ids.length; i++) {
	    var currl = idShapeMap[currp.link_ids[i]];
	    currl.setStroke({style: "Solid", width: 3, cap: "round", color: "red"});
	    currl.moveToFront();

            chunks[i] = surface.createRect({x: currl.shape.x1-3,
					    y: currl.shape.y1-3,
					    width: 8,
					    height: 8
					   });
	    chunks[i].setFill("darkgreen");
	    
	    var diffx = currl.shape.x2 - currl.shape.x1;
	    var diffy = currl.shape.y2 - currl.shape.y1;
	    
            anims[i] = dojox.gfx.fx.animateTransform({
							 shape : chunks[i],
							 duration : 2000, //ms
							 transform: [
							     {name : "translate", start : [0, 0], end:[diffx,diffy]}
							 ]
						     });
	    
            anims2[i] = dojox.gfx.fx.animateTransform({
							  shape : chunks[i],
							  duration : 10, //ms
							  transform: [
							      {name : "translate", start : [diffx,diffy], end:[0,0]}
							  ]
						      });
	    
            dojo.connect(anims[i], "onEnd", anims2[i], "play");
	    dojo.connect(anims2[i], "onEnd", anims[i], "play");
            anims[i].play();
	}
    }
    else {
	return;
    }
}

function devisualizeTransferPath(e) {
    var selectedRow = transferGrid.getItem(prev_row);
    
    if (!selectedRow) {
	return;
    }

    if (path_text) {
	path_text.removeShape();
    }

    var ind = -1;
    for (var i=0; i<paths.length; i++) {
        if (paths[i].t_id == selectedRow.t_id) {
            ind = i;
            break;
        }
    }

    if (ind >= 0) {
        var currp = paths[i];
        var srcNode = idShapeMap[currp.src_id];
        var dstNode = idShapeMap[currp.dst_id];
	
        srcNode.children[0].setFill(topoStore._itemsByIdentity[currp.src_id].fill[0]);
        dstNode.children[0].setFill(topoStore._itemsByIdentity[currp.dst_id].fill[0]);

        for (var i=0; i<currp.link_ids.length; i++) {
            var currl = idShapeMap[currp.link_ids[i]];
            currl.setStroke({style: "Solid", width: 2, cap: "round", color: "black"});
	    if (chunks[i]) {
		chunks[i].removeShape();
	    }
	}
    }
    else {
        return;
    }    
}

function visualizePath(e) {
    if (pathLinks['wanLine'])
	return;

    var selectedRow = circuitGrid.getItem(e.rowIndex);	

    if (prev_row == e.rowIndex) {
        return;
    }
    else {
        prev_row = e.rowIndex;
    }
    
    function doVLAN(items) {
	if (items.length != 2)
	    return;
	
	var o1 = items[0];
	var o2 = items[1];
	
	port1 = idShapeMap[topoStore.getValue(o1, 'id')];
	port2 = idShapeMap[topoStore.getValue(o2, 'id')];
	
	wanLine = surface.createLine({x1: o1.x, y1: o1.y, x2: o2.x, y2: o2.y});
	wanLine.setStroke({style: "Dash", width: 2, cap: "round", color: "green"});
	
	port1.children[0].setFill("green");
	port2.children[0].setFill("green");
	
	pathLinks['wanLine'] = wanLine;
    }
    
    function doEndPoints(items) {
	for (var i = 0; i < items.length; i++) {
	    var o1 = items[i];
	    var node1 = idShapeMap[topoStore.getValue(o1, 'id')];
	    node1.children[0].setFill("orange");
	}
    }	
    
    var regex = new RegExp(selectedRow.vlan);
    topoStore.fetch({
	    query: {name: regex},
		queryOptions: {ignoreCase: true},
		onComplete: doVLAN
		});
    
    var regex = new RegExp("^"+selectedRow.src+"$|^"+selectedRow.dst+"$");
    topoStore.fetch({
	    query: {name: regex},
		queryOptions: {ignoreCase: true},
		onComplete: doEndPoints
		});
}

function devisualizePath(e) {

    var selectedRow = circuitGrid.getItem(prev_row);
    
    function doVLAN(items) {
	if (items.length != 2)
	    return;

        var o1 = items[0];
        var o2 = items[1];
        
        port1 = idShapeMap[topoStore.getValue(o1, 'id')];
        port2 = idShapeMap[topoStore.getValue(o2, 'id')];
        
        port1.children[0].setFill("white");
        port2.children[0].setFill("white");
        
        pathLinks['wanLine'].removeShape();
        pathLinks['wanLine'] = null;
    }
    
    function doEndPoints(items) {
        for (var i = 0; i < items.length; i++) {
            var o1 = items[i];
            var node1 = idShapeMap[topoStore.getValue(o1, 'id')];
            node1.children[0].setFill("aliceblue");
        }
    }
    
    var regex = new RegExp(selectedRow.vlan);
    topoStore.fetch({
	    query: {name: regex},
		queryOptions: {ignoreCase: true},
		onComplete: doVLAN
		});
    
    var regex = new RegExp("^"+selectedRow.src+"$|^"+selectedRow.dst+"$");
    topoStore.fetch({
	    query: {name: regex},
		queryOptions: {ignoreCase: true},
		onComplete: doEndPoints
		});
}

function colorPort(items) {
    for (var i=0; i < items.length; i++) {
        var shape = idShapeMap[topoStore.getValue(items[i], 'id')];
        var port = shape.children[0];
        port.setFill("black").setStroke("red");
    }
}

function decolorPort(items) {
    for (var i=0; i < items.length; i++) {
        var shape = idShapeMap[topoStore.getValue(items[i], 'id')];
        var port = shape.children[0];
        port.setFill("white").setStroke("black");
    }
}

function colorNode(items) {
    for (var i=0; i < items.length; i++) {
        var shape = idShapeMap[topoStore.getValue(items[i], 'id')];
        var port = shape.children[0];
        port.setStroke({color: "black", width: 2});
    }
}

function decolorNode(items) {
    for (var i=0; i < items.length; i++) {
        var shape = idShapeMap[topoStore.getValue(items[i], 'id')];
        var port = shape.children[0];
        port.setStroke("black");
    }
}

function portFront(items) {
    for (var i=0; i < items.length; i++) {
	var shape = idShapeMap[topoStore.getValue(items[i], 'id')];
	shape.moveToFront();
	var port = shape.children[0];
	port.moveToFront();
	port.setStroke("black");
    }
}

function createWAN(items) {
    
    var o1 = items[0];
    var o2 = items[1];
    
    var less_x;
    if (o1.x < o2.x)
	less_x = o1.x[0];
    else
	less_x = o2.x[0];
    
    var less_y;
    if (o1.y < o2.y)
	less_y = o1.y[0];
    else
	less_y = o2.y[0];
    
    var mid_x = (Math.abs(o1.x - o2.x)) / 2 + less_x;
    var mid_y = (Math.abs(o1.y - o2.y)) / 2 + less_y;
    
    wanLine = surface.createLine({x1: o1.x, y1: o1.y, x2: o2.x, y2: o2.y});
    wanLine.setStroke({style: "Dash", width: 2, cap: "round"}, "black");
    wanLine.moveToBack();   
}

function connectNodes(n1, n2, lwidth){
    var o1 = n1.children[0].getShape();
    var o2 = n2.children[0].getShape();

    var o1_points = pointsOnCircle([o1.cx, o1.cy], o1.r, 40);
    var o2_points = pointsOnCircle([o2.cx, o2.cy], o2.r, 40);

    var m_points = closestPoints(o1_points, o2_points);

    //var line = surface.createLine({x1: o1.cx, y1: o1.cy, x2: o2.cx, y2: o2.cy});
    var line = surface.createLine({x1: o1_points[m_points[0]][0], y1: o1_points[m_points[0]][1],
				   x2: o2_points[m_points[1]][0], y2: o2_points[m_points[1]][1]});
    line.setStroke({style: "Solid", width: lwidth, cap: "round", color: "black"});
    return line;
}

function makeLinks(items, request) {
    if(surface) {
	var i;
	for(i = 0; i < items.length; i++) {
	    var linkItem = items[i];
	    
	    var linkId = topoStore.getValue(linkItem, 'id');
	    var linkSource = topoStore.getValue(linkItem, 'source', '');
	    var linkSink = topoStore.getValue(linkItem, 'sink', '');
	    
	    if(!(linkSource && linkSink)) {
		continue;
	    }
	    
	    var linkSourceCap = topoStore.getValue(linkSource, 'capacity', '');
            var linkSinkCap = topoStore.getValue(linkSink, 'capacity', '');

            var linkCap = Math.min(linkSourceCap, linkSinkCap);

            // 1, 8, and 10 Gbps links
            var lwidth = 2;
            if (linkCap == 10e9) { lwidth = 5; }
            else if (linkCap == 8e9) { lwidth = 3; }
            else if (linkCap == 1e9) { lwidth = 2; }

	    var source = idShapeMap[topoStore.getValue(linkSource, 'id')];
	    var sink = idShapeMap[topoStore.getValue(linkSink, 'id')];
	    
	    idShapeMap[linkId] = connectNodes(source, sink, lwidth);
	}
    }
};

function movePorts(items, request) {

	for (var i = 0; i < items.length; i++) {
        	topoStore.fetch({
        		query: { type: "link", source: items[i] },
                                onComplete: moveLinks,
                                dxshift: request['dxshift'],
                                dyshift: request['dyshift'],
		                mports: "true"
        	});
		topoStore.fetch({
        		query: { type: "link", sink: items[i] },
                                onComplete: moveLinks,
                                dxshift: request['dxshift'],
                                dyshift: request['dyshift'],
		                mports: "true"
        	});
	}
	// find those ports that have no links
	for (var i = 0; i < items.length; i++) {
		var sPort = items[i];
		if (!sPort.moved) {
                	topoStore.setValue(sPort, 'x', sPort.x[0] + request['dxshift']);
                    	topoStore.setValue(sPort, 'y', sPort.y[0] + request['dyshift']);

			// now set new port shape coords
			var portShape = idShapeMap[topoStore.getValue(sPort, 'id')].children[0];
			portShape.setShape({cx: sPort.x[0] + request['dxshift'],
				            cy: sPort.y[0] + request['dyshift']});
		}
		sPort.moved = 0;
	}
}

function moveLinks(items, request) {
    
    if (request['mports'] == "true")
	updateLinkPortsPos(items, request);	

    for(var i = 0; i < items.length; i++) {
	var linkItem = items[i];
	
	if (linkItem.incomplete == 1) {
		continue;
	}

	var linkId = topoStore.getValue(linkItem, 'id');
	var linkShape = idShapeMap[linkId];
	var s = linkShape.getShape();
	
	var linkSource = topoStore.getValue(linkItem, 'source', '');
        var linkSink = topoStore.getValue(linkItem, 'sink', '');

        if(!(linkSource && linkSink)) {
                continue;
        }

	var portSource = topoStore.getValue(linkSource, 'id');
        var portSink = topoStore.getValue(linkSink, 'id');

	if (!(portSource && portSink)) {
		continue;
	}

	var sourcePortShape = idShapeMap[portSource];
	var sinkPortShape = idShapeMap[portSink];

	var o1 = sourcePortShape.children[0].getShape();
        var o2 = sinkPortShape.children[0].getShape();

        var o1_points = pointsOnCircle([o1.cx, o1.cy], o1.r, 40);
        var o2_points = pointsOnCircle([o2.cx, o2.cy], o2.r, 40);

        var m_points = closestPoints(o1_points, o2_points);

	linkShape.setShape({x1: o1_points[m_points[0]][0], y1: o1_points[m_points[0]][1], 
		     	    x2: o2_points[m_points[1]][0], y2: o2_points[m_points[1]][1]});
    }
};

// update all the port-pair positions
function updateLinkPortsPos(items, request) {
        for (var i = 0; i < items.length; i++) {
            var shapeItem = items[i];

	    var sourcePortItem = shapeItem.source[0];
	    var sinkPortItem = shapeItem.sink[0];

	    if (!(sourcePortItem && sinkPortItem)) {
		shapeItem.incomplete = 1;
		continue;
	    }
	
            var sourcePort = topoStore.getValue(sourcePortItem, 'id');
            var sinkPort = topoStore.getValue(sinkPortItem, 'id');
	    
	    if (!(sourcePort && sinkPort)) {
		continue;
	    }

	    var sourcePortShape = idShapeMap[sourcePort].children[0];
	    var sinkPortShape = idShapeMap[sinkPort].children[0];
	    
            var sourceNode = sourcePortItem.parent[0];
            var sinkNode = sinkPortItem.parent[0];

	    if (!(sourceNode && sinkNode)) {
		continue;
	    }

            var sourceNodePoint = [ sourceNode.x[0], sourceNode.y[0] ];
            var sinkNodePoint = [ sinkNode.x[0], sinkNode.y[0] ];

	    var sourceWidth =  sourceNode.width[0];
	    var sinkWidth = sinkNode.width[0];

	    // let's get 40 points around each node...
            var source_points = pointsOnCircle(sourceNodePoint, sourceWidth, 40);
            var sink_points = pointsOnCircle(sinkNodePoint, sinkWidth, 40);

            // now find the closest points for the link
            var m_points = closestPoints(source_points, sink_points);

	    sourcePortShape.setShape({cx: source_points[m_points[0]][0], cy: source_points[m_points[0]][1]});
   	    sinkPortShape.setShape({cx: sink_points[m_points[1]][0], cy: sink_points[m_points[1]][1]});

	    //save new port position
	    topoStore.setValue(sourcePortItem, 'x', source_points[m_points[0]][0]);
	    topoStore.setValue(sourcePortItem, 'y', source_points[m_points[0]][1]);
	    topoStore.setValue(sinkPortItem, 'x', sink_points[m_points[1]][0]);
	    topoStore.setValue(sinkPortItem, 'y', sink_points[m_points[1]][1]);

	    sourcePortItem.moved = 1;
	    sinkPortItem.moved = 1;	
        }
};

function makeShapes(items, request) {
    if(surface) {
	var i;
	for(i = 0; i < items.length; i++) {
	    var shapeItem = items[i];
	    // for now we only plot what's manually specified
	    if(!topoStore.hasAttribute(shapeItem, 'shape')) { continue; }
	    
	    if(request['parentGroup']) {
		var shapeGroup = request['parentGroup'].createGroup();
	    } else {
		var shapeGroup = surface.createGroup();
	    }
	    
	    var shape = topoStore.getValue(shapeItem, 'shape', 'circle');
	    var shapeX = topoStore.getValue(shapeItem, 'x', 50);
	    var shapeY = topoStore.getValue(shapeItem, 'y', 50);
	    var shapeWidth = topoStore.getValue(shapeItem, 'width', 30);
	    var shapeHeight = topoStore.getValue(shapeItem, 'height', 30);
	    var shapeFill = topoStore.getValue(shapeItem, 'fill', 'aliceblue');
	    var shapeTextXDisp = topoStore.getValue(shapeItem, 'textXDisp', 0);
	    var shapeTextYDisp = topoStore.getValue(shapeItem, 'textYDisp', 0);
	    var shapeTextAlign = topoStore.getValue(shapeItem, 'textAlign', 'middle');
	    
	    var shapeId = topoStore.getValue(shapeItem, 'id', '');
	    var objectType = topoStore.getValue(shapeItem, 'type', '');
	    var shapeName = topoStore.getValue(shapeItem, 'name', '');
	    var shapeUnisId = topoStore.getValue(shapeItem, 'unisId', shapeName);

	    if(shape == 'rect') {
		shapeGroup.createRect({x: shapeX, y: shapeY, width: shapeWidth, height:shapeHeight}).setStroke("black").setFill(shapeFill);
	    } else if (shape == 'circle') {
		var newCircle = shapeGroup.createCircle({cx: shapeX, cy: shapeY, r: shapeWidth}).setStroke("black").setFill(shapeFill);
		newCircle.getEventSource().id = shapeUnisId;
	    }
	    
	    if(objectType == 'port') {
		var portDisplay = topoStore.getValue(shapeItem, 'display', shapeName);
		new periscope.Tooltip(shapeGroup.children[0], { text: portDisplay });
		
		chart_window_event(newCircle);
	
		dojo.connect(newCircle.getEventSource(), "onmouseover", null, function(e) {
			topoStore.fetch({query: {"unisId": e.target.id}, onComplete: colorPort});
		    });

		dojo.connect(newCircle.getEventSource(), "onmouseleave", null, function(e) {
                        topoStore.fetch({query: {"unisId": e.target.id}, onComplete: decolorPort});
                    });

		// make ports moveable
                var m = new dojox.gfx.Moveable(newCircle);
                m.shapeItem = shapeItem;
		
                dojo.connect(m, "onMoved", function(mover, shift){

                    //save the new shape position
                    var port = mover.host.shapeItem;
                    topoStore.setValue(port, 'x', port.x[0] + shift.dx);
                    topoStore.setValue(port, 'y', port.y[0] + shift.dy);
		    
		    /*
		    topoStore.fetch({
                        query: { type: "link", source: port },
                        onComplete: moveLinks,
                        dxshift: request['dxshift'],
                        dyshift: request['dyshift'],
                        mports: "false"
                    });
                    topoStore.fetch({
                        query: { type: "link", sink: port },
                        onComplete: moveLinks,
                        dxshift: request['dxshift'],
                        dyshift: request['dyshift'],
                        mports: "false"
                    });
		    */
		});
	    } 
	    else {
		    var text = shapeGroup.createText({
				    x: shapeX+shapeTextXDisp,
				    y: shapeY+shapeTextYDisp,
				    text: shapeName,
				    align: shapeTextAlign});
		    text.setFont({family: "Helvetica", size: "8pt", weight: "bold"});
		    text.setFill("black");
		    
		if (objectType == 'node') {
		    
		    text.getEventSource().id = shapeUnisId;

		    dojo.connect(text.getEventSource(), "onmouseover", null, function(e) {
                            topoStore.fetch({query: {"unisId": e.target.id}, onComplete: colorNode});
                        });

                    dojo.connect(text.getEventSource(), "onmouseleave", null, function(e) {
                            topoStore.fetch({query: {"unisId": e.target.id}, onComplete: decolorNode});
                        });

		    dojo.connect(newCircle.getEventSource(), "onmouseover", null, function(e) {
			    topoStore.fetch({query: {"unisId": e.target.id}, onComplete: colorNode});
			});
		    
		    dojo.connect(newCircle.getEventSource(), "onmouseleave", null, function(e) {
			    topoStore.fetch({query: {"unisId": e.target.id}, onComplete: decolorNode});
			});
		    
		    dojo.connect(newCircle.getEventSource(), "ondblclick", null, makePane);
		    dojo.connect(text.getEventSource(), "ondblclick", null, makePane);

		    // make nodes moveable
                    var m = new dojox.gfx.Moveable(newCircle);
                    m.shapeItem = shapeItem;
	            
		    dojo.connect(m, "onMoved", function(mover, shift){
	
	                //first we save the new shape position
	                var node = mover.host.shapeItem;
			topoStore.setValue(node, 'x', node.x[0] + shift.dx);
			topoStore.setValue(node, 'y', node.y[0] + shift.dy);

			//move text along with node
			// XXX need to make text selectable for move too...*sigh*
			var textShape = idShapeMap[topoStore.getValue(node, 'id')].children[1]; 
			var s = textShape.getShape();
			textShape.setShape({x: s.x + shift.dx, y: s.y + shift.dy});			

                        topoStore.fetch({
                            query: { type: "port", parent: node },
                                onComplete: movePorts,
                                dxshift: shift.dx,
                                dyshift: shift.dy
                                });
 	            	}
		   );
		}
	    }
	    
	    idShapeMap[shapeId] = shapeGroup;
	    
	    topoStore.fetch({
		    query: { parent: shapeItem },
			onComplete: makeShapes,
			parentGroup: shapeGroup
			});
	}
    }
};


/*
 * Updates link's color by UNIS Id
 */
function updateLinkColor(urn, color) {
    var linkId;
    var getLinkId = function (items) {
          if (items.length == 1)  {
               linkId = items[0]['id'][0];
          } else {
              console.error("No link found of urn " + urn );
          }
    };
   
    try {
        topoStore.fetch({query: {unisId: urn}, onComplete: getLinkId});
        var linkShape = idShapeMap[linkId];
        var stroke = linkShape.getStroke();
        stroke['color'] = color;
        linkShape.setStroke(stroke);
        linkShape.setFill(color);
    } catch (err) {
        console.error("Error at urn: " + urn);
        console.error(err);
    }
}
