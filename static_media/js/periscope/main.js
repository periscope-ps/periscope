// top-level js for periscope topology drawing

//====================================================
// some globals

// the topology store
var topoStore;
// the surface to draw on
var surface;
// the shape map
var idShapeMap = {};

//====================================================

dojo.require("dojo.data.ItemFileWriteStore");
dojo.require("dojo.data.ItemFileReadStore");
dojo.require("dojox.widget.AnalogGauge");
dojo.require("dojox.widget.gauge.AnalogArcIndicator");
dojo.require("dojox.widget.gauge.AnalogNeedleIndicator");
dojo.require("dojox.timing._base");

function include(jsFile)
{
	document.write('<script type="text/javascript" src="'
		       + jsFile + '"></script>'); 
}


function createUNISTopoStore(topo_items) {

	topoStore = new dojo.data.ItemFileWriteStore({data: {
				"label": "unisId",
				"identifier": "id",
				"items": topo_items
			}});
}

function initGfx(request) {
        container = dojo.byId("topo");
        surface = dojox.gfx.createSurface(container, request['width'], request['height']);
        surface_size = {width: request['width'], height: request['height']};

        //console.log(request);

        if (request['background']) {
		set_surface_background(request['background']);
	}

	var level = "node";
	if (request['level']) {
		level = request['level'];
	}
	
	if (request['spring']=="true") {
		topoStore.fetch({
				query: { type: "node" },
					onComplete: doSpring
					});
		
	}
	
	topoStore.fetch({
			query: { type: level },
				onComplete: makeShapes
				});

	topoStore.fetch({
                        query: { type: "link" },
				onComplete: makeLinks
				});

	if (request['movePorts']=="true") {
		topoStore.fetch({
                                query: { type: "port" },
					onComplete: movePorts,
					dxshift: 0,
					dyshift: 0
					});
	}

        // cancel text selection and text dragging
        dojo.connect(container, "ondragstart",   dojo, "stopEvent");
        dojo.connect(container, "onselectstart", dojo, "stopEvent");
};

function add_surface_text(request) {

    var surface_text_group = surface.createGroup();    

    var s_dim = surface.getDimensions();    

    var box = surface_text_group.createRect({
						x: request['x']-3,
						y: request['y']-25,
						width: s_dim.width - 20, 
						height: 40});
    box.setStroke("black").setFill(request['bg']);

    var surface_text = surface_text_group.createText({
					      x: request['x'],
					      y: request['y'],
					      text: request['text'],
					      align: request['align']});
    surface_text.setFont({family: request['font'], size: request['size'], weight: request['weight']});
    surface_text.setFill(request['fill']);
    
    return surface_text_group;
}

function set_surface_background(image) {
	if (surface) {
		var s_dim = surface.getDimensions();
		var bg = surface.createImage({x: 0, 
					     y: 0,	
                			     width: s_dim.width,
					     height: s_dim.height,
                			     src: image});
		bg.moveToBack();
	}
}

include('/static_media/js/periscope/view.js');
include('/static_media/js/periscope/grid.js');
include('/static_media/js/periscope/pane.js');
include('/static_media/js/periscope/spring.js');