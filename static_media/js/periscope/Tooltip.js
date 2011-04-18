// Adapted from dojox.charting.action2d.Tooltip

dojo.provide("periscope.Tooltip");

dojo.require("dojox.charting.action2d.Base");
dojo.require("dojox.gfx.matrix");
dojo.require("dijit.Tooltip");

dojo.require("dojox.lang.functional");
dojo.require("dojox.lang.functional.scan");
dojo.require("dojox.lang.functional.fold");

/*=====
dojo.declare("dojox.charting.action2d.__TooltipCtorArgs", dojox.charting.action2d.__BaseCtorArgs, {
	//	summary:
	//		Additional arguments for tooltip actions.

	//	text: Function?
	//		The function that produces the text to be shown within a tooltip.  By default this will be 
	//		set by the plot in question, by returning the value of the element.
	text: null
});
=====*/
(function(){
	
	var df = dojox.lang.functional, m = dojox.gfx.matrix, pi4 = Math.PI / 4, pi2 = Math.PI / 2;
	
	dojo.declare("periscope.Tooltip", null, {
		//	summary:
		//		Create an action on a plot where a tooltip is shown when hovering over an element.

		// the data description block for the widget parser
		defaultParams: {}, // no default parameters
		optionalParams: {},	// no optional parameters

		constructor: function(shape, kwArgs){
			//	summary:
			//		Create the tooltip action and connect it to the shape.
			//	shape: dojox.gfx.Shape
			//		The shape this tooltip belongs to.
			//	kwArgs:
			//		Optional keyword arguments object for setting parameters.
			
			this.shape = shape;
			this.text = kwArgs && kwArgs.text ? kwArgs.text : '';
			
			this.connect();
		},
		
		connect: function(){
			//	summary:
			//		Connect this action to the given shape.
			this.shape.connect("onmouseover", this, function(e){
				this.process("onmouseover", e);
			});
			this.shape.connect("onmouseout", this, function(e){
				this.process("onmouseout", e);
			});
		},
		
		process: function(eventType, e){
			//	summary:
			//		Process the action on the given object.
			//	o: dojox.gfx.Shape
			//		The object on which to process the highlighting action.
			if(eventType === "onmouseout"){
				hideChartingTooltip(this.aroundRect);
				this.aroundRect = null;
				return;
			}
			
			if(!this.shape || eventType !== "onmouseover"){ return; }
			
			// calculate relative coordinates and the position
			var aroundRect = {type: "rect"}, position = ["after", "before"];
			var bbox = this.shape.getBoundingBox();
			aroundRect.x = bbox.x;
			aroundRect.y = bbox.y;
			aroundRect.width = bbox.width; 
			aroundRect.height = bbox.height;
			
			// adjust relative coordinates to absolute, and remove fractions
			var parent = this.shape;
			while(parent.parent != null) { parent = parent.parent; }
			var lt = dojo.coords(parent.getEventSource(), true);
			aroundRect.x += lt.x;
			aroundRect.y += lt.y;
			aroundRect.x = Math.round(aroundRect.x);
			aroundRect.y = Math.round(aroundRect.y);
			aroundRect.width = Math.ceil(aroundRect.width);
			aroundRect.height = Math.ceil(aroundRect.height);
			this.aroundRect = aroundRect;
			
			showChartingTooltip(this.text, this.aroundRect, position, "center");
		}
	});
	
	//TODO: make the charting tooltip a generic one so it can be used with
	// dojox.gfx shapes without charting.
	
	var MasterTooltip = dojo.declare(dijit._MasterTooltip, {
		
		show: function(/*String*/ innerHTML, /*DomNode*/ aroundNode, /*String[]?*/ position, /*String*/alignment){
			// summary:
			//		Display tooltip w/specified contents to right of specified node
			//		(To left if there's no space on the right, or if LTR==right)
			// alignment: String
			//		"center":   tooltip center alignment
			//      "default":  tooltip default alignment (left, right, top, bottom)

			if(this.aroundNode && this.aroundNode === aroundNode){
				return;
			}

			if(this.fadeOut.status() == "playing"){
				// previous tooltip is being hidden; wait until the hide completes then show new one
				this._onDeck=arguments;
				return;
			}
			this.containerNode.innerHTML=innerHTML;

			// Firefox bug. when innerHTML changes to be shorter than previous
			// one, the node size will not be updated until it moves.
			this.domNode.style.top = (this.domNode.offsetTop + 1) + "px";
			
			if(!this.connectorNode) this.connectorNode = dojo.query(".dijitTooltipConnector", this.domNode)[0];
			var connectorPos = dojo.coords(this.connectorNode);
			this.arrowWidth = connectorPos.w, this.arrowHeight = connectorPos.h;
			this.place = (alignment && alignment == "center") ? this.placeChartingTooltip : dijit.placeOnScreenAroundElement,
			this.place(
				this.domNode,
				aroundNode,
				dijit.getPopupAroundAlignment(
					(position && position.length) ? position : dijit.Tooltip.defaultPosition,
					this.isLeftToRight()
				),
				dojo.hitch(this, "orient")
			);

			// show it
			dojo.style(this.domNode, "opacity", 0);
			this.fadeIn.play();
			this.isShowingNow = true;
			this.aroundNode = aroundNode;
		},
		
		placeChartingTooltip: function(node, aroundRect, aroundCorners, layoutNode){
			return this._placeOnScreenAroundRect(node, 
				aroundRect.x, aroundRect.y, aroundRect.width, aroundRect.height,	// rectangle
				aroundCorners, layoutNode);
		},
		
		_placeOnScreenAroundRect: function(node, x, y, width, height, aroundCorners, layoutNode){
			var choices = [];
		    for (var nodeCorner in aroundCorners) {
		        choices.push({
		            aroundCorner: nodeCorner,
		            corner: aroundCorners[nodeCorner],
		            pos: {
		                x: x + (nodeCorner.charAt(1) == 'L' ? 0 : width),
		                y: y + (nodeCorner.charAt(0) == 'T' ? 0 : height),
		                w: width,
		                h: height
		            }
		        });
		    }
		    return this._place(node, choices, layoutNode);
		},
		
		_place: function(/* DomNode */node, /* Array */ choices, /* Function */ layoutNode){
		    var view = dijit.getViewport();
		    
		    if (!node.parentNode ||
		    String(node.parentNode.tagName).toLowerCase() != "body") {
		        dojo.body().appendChild(node);
		    }
		    
		    var best = null;
		    
		    var arrowLeft = null, arrowTop = null;
		    dojo.some(choices, function(choice){
		        var corner = choice.corner;
		        var aroundCorner = choice.aroundCorner;
		        var pos = choice.pos;
		        
		        if (layoutNode) {
		            layoutNode(node, choice.aroundCorner, corner);
		        }
		        
		        // get node's size
		        var style = node.style;
		        var oldDisplay = style.display;
		        var oldVis = style.visibility;
		        style.visibility = "hidden";
		        style.display = "";
		        var mb = dojo.marginBox(node);
		        style.display = oldDisplay;
		        style.visibility = oldVis;
		        
		        var startX, startY, endX, endY, width, height, overflow;
		        
		        arrowLeft = null, arrowTop = null;
		        if (aroundCorner.charAt(0) == corner.charAt(0)) { //left, right
		            startX = (corner.charAt(1) == 'L' ? pos.x : Math.max(view.l, pos.x - mb.w)), 
					startY = (corner.charAt(0) == 'T' ? (pos.y + pos.h / 2 - mb.h / 2) : (pos.y - pos.h / 2 - mb.h / 2)), 
					endX = (corner.charAt(1) == 'L' ? Math.min(view.l + view.w, startX + mb.w) : pos.x), 
					endY = startY + mb.h, 
					width = endX - startX, 
					height = endY - startY, 
					overflow = (mb.w - width) + (mb.h - height);
		            arrowTop = (mb.h - this.arrowHeight) / 2;
		        }
		        else { //top, bottom
		            startX = (corner.charAt(1) == 'L' ? (pos.x + pos.w / 2 - mb.w / 2) : (pos.x - pos.w / 2 - mb.w / 2)), 
					startY = (corner.charAt(0) == 'T' ? pos.y : Math.max(view.t, pos.y - mb.h)), 
					endX = startX + mb.w, 
					endY = (corner.charAt(0) == 'T' ? Math.min(view.t + view.h, startY + mb.h) : pos.y), 
					width = endX - startX, 
					height = endY - startY, 
					overflow = (mb.w - width) + (mb.h - height);
		            arrowLeft = (mb.w - this.arrowWidth) / 2;
		        }
		        
		        if (best == null || overflow < best.overflow) {
		            best = {
		                corner: corner,
		                aroundCorner: choice.aroundCorner,
		                x: startX,
		                y: startY,
		                w: width,
		                h: height,
		                overflow: overflow
		            };
		        }
		        return !overflow;
		    }, this);
		    
		    node.style.left = best.x + "px";
		    node.style.top = best.y + "px";
		    
			this.connectorNode.style.top = "";
	        this.connectorNode.style.left = "";
	        if (arrowTop){
				this.connectorNode.style.top = arrowTop + "px";
			}
	        if (arrowLeft){
				this.connectorNode.style.left = arrowLeft + "px";
			}
	        
		    if (best.overflow && layoutNode) {
		        layoutNode(node, best.aroundCorner, best.corner);
		    }
		    return best;
		}
	});
	
	var masterTT = null;
	
	function showChartingTooltip(innerHTML, aroundNode, position, alignment){
		if(!masterTT){ masterTT = new MasterTooltip(); }
		return masterTT.show(innerHTML, aroundNode, position, alignment);
	}
	
	function hideChartingTooltip(aroundNode){
		if(!masterTT){ masterTT = new MasterTooltip(); }
		return masterTT.hide(aroundNode);
	}
})();
