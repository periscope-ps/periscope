dojo.require("dojox.layout.FloatingPane");


// global timer since there must be some bug with
// FloatingPane not destroying the timer object on close

var host_t;

function makePane(e) {

	host_t = new dojox.timing.Timer();

	hostPane = new dojox.layout.FloatingPane({
			href: '{% url measurements.views.get_host_info %}?id=' + e.target.id,
			title: "Host information for " + e.target.id,
			resizable: true,
			dockable: false,
			style: "position:absolute;top:200;left:400;width:860px;height:530px;visibility:hidden;",
			id: "hostPane:"+e.target.id
		}, dojo.create("div", null, dojo.body(), "first"));

	hostPane.startup();
	hostPane.show();
	hostPane.refresh();
	hostPane.bringToTop();

	dojo.connect(hostPane, "close", null, function(e) { host_t.stop(); });
}
