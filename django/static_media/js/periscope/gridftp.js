dojo.require("dijit.form.MultiSelect");

//global for current paths
var paths = []

//needle for the Perfometer
var xferNeedle;

initXFERPerfometer = function () {
	var gauge = dijit.byId('XFERPerfometer');
	// Used for a gradient arc indicator below:
	var fill = {
		'type': 'linear',
		'x1': 10,
		'y1': 10,
		'x2': 120,
		'y2': 120,
		'colors': [{
				offset: 0,
				color: 'black'
			},
	{
		offset: 0.5,
		color: 'black'
	},
	{
		offset: 0.65,
		color: 'yellow'
	},
	{
		offset: 1,
		color: 'red'
	}]
	};
	gauge.addIndicator(new dojox.widget.gauge.AnalogArcIndicator({
				'value': 10000,
					'width': 5,
					'offset': 60,
					'color': fill,
					'noChange': true,
					'hideValues': true
					}));
	gauge.addIndicator(new dojox.widget.gauge.AnalogArcIndicator({
				'value': 6500,
					'width': 5,
					'offset': 60,
					'color': 'blue',
					'title': 'Arc',
					'hover': 'Arc: 750'
					}));
	gauge.addIndicator(new dojox.widget.gauge.AnalogNeedleIndicator({
				'value': 0,
					'width': 3,
					'length': 60,
					'color': 'red',
					'title': 'rate',
					'hover': 'rate: 0'
					}));
};

initUserSelect = function () {

        var msel = new dijit.form.MultiSelect({
			'name': 'usersel',
			'size': 17,
			'style': 'width: 150px'
		},
		dojo.byId('usersel'));

        dojo.connect(msel, "onChange", null, function() { 
			var selected = transferGrid.selection.getSelected();
			dojo.forEach(selected, function(selected) {
					var ind = transferGrid.getItemIndex(selected);
					devisualizeTransferPath(ind);
				});			
			prev_row = -1;
			updateTransferGrid();
		});

	updateUserSelect();
	var t = new dojox.timing.Timer();
	t.setInterval(30000);
	t.onTick = updateUserSelect;
	t.start();
};
