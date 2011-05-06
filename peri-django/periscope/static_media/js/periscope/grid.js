dojo.require("dojox.grid.DataGrid");
dojo.require("dojox.timing._base");

// two global grids defined here
var transferGrid;
var circuitGrid;

function initTransferGrid() {

    function doGridHTML(item) {
        return item.replace(/&lt;/gi, "<");
    }

    // set the layout structure:
    var layout = [
{
    field: 't_id',
    name: 'Transfer ID',
    width: '120px'
},
{
    field: 'status',
    name: 'Status',
    width: '50px'
},  
{
    field: 'src',
    name: 'Source',
    width: '150px'
},
{
    field: 'dst',
    name: 'Destination',
    width: '150px'
},
{
    field: 'sport',
    name: 'Source Port',
    width: '120px'
},
{
    field: 'dport',
    name: 'Dest. Port',
    width: '120px'
},
{
    field: 'misc',
    name: 'Misc',
    width: '300px'
},

    ];

    // create a new grid:
    var grid = new dojox.grid.DataGrid({
            query: {
                tId: "*"
            },
            //store: resStore,
            clientSort: true,
            rowSelector: '20px',
            structure: layout
        },
        document.createElement('div'));

    // append the new grid to the div "gridTransferContainer":
    dojo.byId("gridTransferContainer").appendChild(grid.domNode);

    // Call startup, in order to render the grid:
    grid.startup();
    transferGrid = grid;

    grid_window_event(grid);

    dojo.connect(grid, "onRowClick", visualizeTransferPath);
    dojo.connect(grid, "onDeselected", devisualizeTransferPath);

    updateTransferGrid();
    var t = new dojox.timing.Timer();
    t.setInterval(30000);
    t.onTick = updateTransferGrid;
    t.start();
};

function initCircuitGrid() {
    
    function doGridHTML(item) {
	return item.replace(/&lt;/gi, "<");
    }
    
    // set the layout structure:
    var layout = [
{
    field: 'resId',
    name: 'Path ID',
    width: '120px'
},
{
    field: 'status',
    name: 'Status',
    width: '50px'
},
{
    field: 'src',
    name: 'Source',
    width: '100px'
},
{
    field: 'dst',
    name: 'Destination',
    width: '100px'
},
{
    field: 'src-ports',
    name: 'Src ports',
    width: '100px'
},
{
    field: 'dst-ports',
    name: 'Dest ports',
    width: '100px'
},
{
    field: 'direction',
    name: 'Direction',
    width: '100px'
},
{
    field: 'start',
    name: 'Start time',
    width: '150px'
},
{
    field: 'duration',
    name: 'Duration (s)',
    width: '100px'
},
{
    field: 'bw',
    name: 'Bandwidth (bps)',
    width: '100px'
},
{
    field: 'bw-class',
    name: 'BW class',
    width: '70px'
},
{
    field: 'vlan',
    name: 'VLAN',
    width: '50px'
},
    ];

    // create a new grid:
    var grid = new dojox.grid.DataGrid({
	    query: {
                resId: "*"
            },
            //store: resStore,
            clientSort: true,
            rowSelector: '20px',
            structure: layout
        },
        document.createElement('div'));
    
    // append the new grid to the div "gridContainer":
    dojo.byId("gridContainer").appendChild(grid.domNode);
    
    // Call startup, in order to render the grid:
    grid.startup();
    circuitGrid = grid;

    grid_window_event(grid);
    
    dojo.connect(grid, "onRowClick", visualizePath);
    dojo.connect(grid, "onDeselected", devisualizePath);
        
    updateCircuitGrid();
    var t = new dojox.timing.Timer();
    t.setInterval(10000);
    t.onTick = updateCircuitGrid;
    t.start();
};



