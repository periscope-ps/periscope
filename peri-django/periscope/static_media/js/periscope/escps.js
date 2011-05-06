function drawWAN() {
    topoStore.fetch({
	query: { name: /^nile$|^amon$/ },
	onComplete: createWAN
    });
    
    topoStore.fetch({
        query: { name: /^ir1gw$|^amon$/ },
        onComplete: createWAN
    });

    /*
    imageGroup = surface.createGroup();
    imageGroup.createImage({x: mid_x-50, y: mid_y-50, 
			    width: 100, height: 100,
			    src: "/static_media/images/wan_cloud.png"}); 
    text = imageGroup.createText({x: mid_x-20, y: mid_y+5, text: "WAN"});
    text.setFont({family: "Helvetica", size: "12pt", weight: "bold"});
    text.setFill("black");
    */
}

// Two needles for the Rx and Tx Perfometers
var BNLTxNeedle;
var BNLRxNeedle;
var UltralightTxNeedle;
var UltralightRxNeedle;

initBNLPerfometer = function () {
	var gauge = dijit.byId('BNLPerfometer');
	// Used for a gradient arc indicator below:
	var fill = {
		'type': 'linear',
		'x1': 0,
		'y1': 0,
		'x2': 100,
		'y2': 100,
		'colors': [{
				offset: 0,
				color: 'black'
			},
        {
		offset: 0.5,
		color: 'black'
        },
        {
		offset: 0.75,
		color: 'yellow'
        },
        {
		offset: 1,
		color: 'red'
        }]
	};
	gauge.addIndicator(new dojox.widget.gauge.AnalogArcIndicator({
				'value': 100,
					'width': 5,
					'offset': 60,
					'color': fill,
					'noChange': true,
					'hideValues': true
					}));
	gauge.addIndicator(new dojox.widget.gauge.AnalogArcIndicator({
				'value': 75,
					'width': 5,
					'offset': 60,
					'color': 'blue',
					'noChange': true,
					'hover': 'Arc: 75'
					}));
	BNLTxNeedle = gauge.addIndicator(new dojox.widget.gauge.AnalogNeedleIndicator({
				'value': 0,
				'width': 3,
				'length': 60,
				'color': 'red',
				'title': 'Rx%',
				'hover': 'Rx%: 0'
			}));
	BNLRxNeedle = gauge.addIndicator(new dojox.widget.gauge.AnalogNeedleIndicator({
				'value': 0,
				'width': 3,
				'length': 60,
				'color': 'yellow',
				'title': 'Rx%',
				'hover': 'Rx%: 0'
			}));
};

initUltralightPerfometer = function () {
	var gauge = dijit.byId('UltralightPerfometer');
	// Used for a gradient arc indicator below:
	var fill = {
		'type': 'linear',
		'x1': 0,
		'y1': 0,
		'x2': 100,
		'y2': 100,
		'colors': [{
				offset: 0,
				color: 'black'
			},
        {
		offset: 0.5,
		color: 'black'
        },
        {
		offset: 0.75,
		color: 'yellow'
        },
        {
		offset: 1,
		color: 'red'
        }]
	};
	gauge.addIndicator(new dojox.widget.gauge.AnalogArcIndicator({
				'value': 100,
					'width': 5,
					'offset': 60,
					'color': fill,
					'noChange': true,
					'hideValues': true
					}));
	gauge.addIndicator(new dojox.widget.gauge.AnalogArcIndicator({
				'value': 75,
					'width': 5,
					'offset': 60,
					'color': 'blue',
					'noChange': true,
					'hover': 'Arc: 75'
					}));

	UltralightTxNeedle = gauge.addIndicator(new dojox.widget.gauge.AnalogNeedleIndicator({
				'value': 0,
				'width': 3,
				'length': 60,
				'color': 'red',
				'title': 'Tx%',
				'hover': 'Tx%: 50'
			}));
	UltralightRxNeedle = gauge.addIndicator(new dojox.widget.gauge.AnalogNeedleIndicator({
				'value': 0,
				'width': 3,
				'length': 60,
				'color': 'yellow',
				'title': 'Rx%',
				'hover': 'Rx%: 0'
			}));
};
