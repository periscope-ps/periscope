// JavaScript for Stampede workflow analyzer.


$(function() {
    $.ajax({
        url: "/db",
        dataType: 'json',
            data: "",
            success: set_database_name
    });
    get_uuid = function() {
        return $('#uuid').text()
    }
    set_uuid = function(value) {
        $('#uuid').html(value)
    }
    get_sub_uuid = function() {
        return $('#sub_uuid').text()
    }
    set_sub_uuid = function(value) {
        $('#sub_uuid').html(value)
    }
    $('#refresh').click(function() {
        if ($('#subworkflow_view').val()) {
            sub_uuid = get_sub_uuid();
            show_subworkflow_view(sub_uuid, false);
        } else if ($('#subworkflow_list_view').val()) {
            for (i=0; i < 4; i++) {
                $('#summaryChartScroll' + i).empty();
            }
            $('#xformChartScroll').empty();
            plotScroll(data, 'subChartScroll', 'column', true);
        } else if ($('#workflow_view').val()) {
            show_workflow_view(false);
        } else {
            show_root_view(false);
        }
    });
		$("#accordion_wf").accordion({
			collapsible: true,
			active: false
    });
		$("#accordion_xform").accordion({
			collapsible: true,
			active: false
    });
    $('#root_wfs').click(function() {
        show_root_view(true);
    });
    $('#workflow').click(function() {
        show_workflow_view(true);
    });
    $('#subworkflow_list').click(function() {
        $.ajax({
            url: "/wf/" + get_uuid() + "/list",
            dataType: 'json',
                data: "",
                success: show_subworkflows
        });
    });
    $('#subworkflow').click(function() {
        sub_uuid = get_sub_uuid();
        show_subworkflow_view(sub_uuid, true);
    });
    $('#showsub').click(function() {
        $.ajax({
            url: "/wf/" + get_uuid() + "/list",
            dataType: 'json',
                data: "",
                success: show_subworkflows
        });
    });
    $('#subtotals').click(function() {
        for (i=0; i < 4; i++) {
            $('#summaryChartScroll' + i).empty();
        }
        $('#xformChartScroll').empty();
        $.ajax({
            url: get_info_url(get_uuid()),
            dataType: 'json',
            data: "",
            success: show_summary_stats
        });
    });
    $('#selectWorkflow').live('hover',
        function() {
            $('#selectWorkflowHelp').dialog();
        }
    );
    $('#selectSubWorkflow').live('hover',
        function() {
            $('#selectSubWorkflowHelp').dialog();
        }
    );
    $('#summaryWorkflow').live('hover',
        function() {
            $('#summaryWorkflowHelp').dialog({ minWidth: 350 });
        }
    );
});

var summaryChartScroll = new Array(4);
var xformChartScroll;
var subChartScroll;

function get_job_task_stats(celDiv) {
    $(celDiv).click (
        function () {
            // the .trSelected selector does not work for every other td
            var wf_uuid = $(this).parent().parent().attr('id').substring(3);
            set_uuid(wf_uuid);
            var dax_label = $(this).parent().parent().children().children().html();
            $('#sep1').html("&nbsp;->&nbsp;");
            $('#dax_label').html(dax_label);
            $('#workflow').html(dax_label);
            show_workflow_view(true);
        }
    );
}

set_database_name = function(data, text_status, jqxhr) {
    $('#root_wfs').html('Database ' + data.name);
}

// Show job, task, transformation, and sub-workflow bars, and get data for
// transformations accordion
show_summary_stats = function(data, text_status, jqxhr) {
    plotSummaryScroll(data.summary, 0, false);
    plotSummaryScroll(data.summary, 1, false);
    numSubworkflows = data.summary.successful[3];
    numSubworkflows += data.summary.failed[3];
    numSubworkflows += data.summary.incomplete[3];
    if (numSubworkflows > 0) {
        plotSummaryScroll(data.summary, 2, false);
        $("#subcontrols").show();
        plotSummaryScroll(data.summary, 3, true);
    } else {
        plotSummaryScroll(data.summary, 2, true);
    }
    plotTransformScroll(data.xforms, 'xformChartScroll', 'bar');
}

show_transformations = function(data, text_status, jqxhr) {
    plotTransformScroll(data, 'xformChartScroll', 'bar');
}

show_subworkflows = function(data, text_status, jqxhr) {
    $('#sep2').html("&nbsp;->&nbsp;");
    $('#subworkflow_list').html('sub-workflows');
    $('#rootContainer').hide();
    $('#subContainer').show();
    $('#accordion_wf_title').html('Select a sub-workflow ' + '<span id="selectSubWorkflow">[?]<span>');
    $("#accordion_wf").accordion({
        active: false 
    });
    $("#subcontrols").hide();
    $('#accordion_xform').hide()
    $("#accordion_xform").accordion({
         active: false
    });
    for (i=0; i < 4; i++) {
        $('#summaryChartScroll' + i).empty();
    }
    $('#xformChartScroll').empty();
    plotScroll(data, 'subChartScroll', 'column', true);
    return;
}

plotScroll = function(data, id, orientation, handleClick) {
    if (id == 'xformChartScroll') {
        var plot = xformChartScroll;
    } else if (id == 'subChartScroll') {
        var plot = subChartScroll;
    }
    var jobstate = ['Success','Incomplete','Failure'];
    $('#' + id).empty();
    var n = data.num; // number of bars
    if (orientation != 'column') {
        document.getElementById(id).style.height = n * 30;
    }
    plot = new Highcharts.Chart({
        chart: {
            renderTo: id,
            defaultSeriesType: orientation
        },
        title: {
            text: ''
        },
        credits: {
            enabled: false
        },
        tooltip: {
            formatter: function() {
                if (handleClick) {
                    return this.series.name + ': ' + this.point.y + '<br/>uuid: ' + this.point.uuid;
                } else  {
                    return this.series.name + ': ' + this.point.y;
                }
            }
        },
        xAxis: {
            categories: data.names
        },
        yAxis: {
            min:0,
            title: {
                text: ''
           }
        }, 
        legend: {
            backgroundColor: '#FFFFFF',
            reversed: true
        },
        plotOptions: {
            area: {
                shadow: false
            },
            bar: {
                borderWidth: 0
            },
            column: {
                borderWidth: 0
            },
            series: {
                stacking: 'normal',
                animation: false,
                point: {
                    events: {
                        click: function() {
                            if (handleClick) {
                                show_subworkflow_info(this.category, this.uuid);
                            }
                        }
                    }
                }
            }
        },
        colors: [
            'rgba(0, 200, 0, 0.8)',
            'rgba(200, 200, 0, 0.8)',
            'rgba(255, 0, 0, 0.8)'
        ],
        series: [
        {
            name: 'Successful',
            data: data.successful
        },
        {
            name: 'Incomplete',
            data: data.incomplete
        },
        {
            name: 'Failed',
            data: data.failed
        }]
    });
}

plotSummaryScroll = function(data, indx, showLegend) {
    names = [data.names[indx]];
    successful = [data.successful[indx]];
    incomplete = [data.incomplete[indx]];
    failed = [data.failed[indx]];
    var plot = summaryChartScroll[indx];
    var jobstate = ['Success','Incomplete','Failure'];
    $('#summaryChartScroll' + indx).empty();
    if (showLegend) {
        document.getElementById("summaryChartScroll" + indx).style.height = 85;
    } else {
        document.getElementById("summaryChartScroll" + indx).style.height = 50;
    }
    plot = new Highcharts.Chart({
        chart: {
            renderTo: 'summaryChartScroll' + indx,
            defaultSeriesType: 'bar'
        },
        title: {
            text: ''
        },
        credits: {
            enabled: false
        },
        tooltip: {
            formatter: function() {
                return this.series.name + ': ' + this.point.y;
            }
        },
        xAxis: {
            categories: names
        },
        yAxis: {
            min:0,
            title: {
                text: ''
           }
        }, 
        legend: {
            enabled: showLegend,
            backgroundColor: '#FFFFFF',
            reversed: true
        },
        plotOptions: {
            area: {
                shadow: false
            },
            bar: {
                borderWidth: 0
            },
            series: {
                stacking: 'normal',
                animation: false,
            }
        },
        colors: [
            'rgba(0, 200, 0, 0.8)',
            'rgba(200, 200, 0, 0.8)',
            'rgba(255, 0, 0, 0.8)'
        ],
        series: [
        {
            name: 'Successful',
            data: successful
        },
        {
            name: 'Incomplete',
            data: incomplete
        },
        {
            name: 'Failed',
            data: failed
        }]
    });
}

function log10(n) {
     return Math.log(n)/Math.log(10);   
}

plotTransformScroll = function(data, id, orientation) {
    var plot = xformChartScroll;
    var jobstate = ['Success','Incomplete','Failure'];
    $('#' + id).empty();
    var n = data.num; // number of bars
    var max = 0
    for (var i=0; i < data.successful.length; i++) {
        if (data.successful[i] > max) {
            max = data.successful[i];
        }
    }
    for (var i=0; i < data.incomplete.length; i++) {
        if (data.incomplete[i] > max) {
            max = data.incomplete[i];
        }
    }
    for (var i=0; i < data.failed.length; i++) {
        if (data.failed[i] > max) {
            max = data.failed[i];
        }
    }
    if (max > 25) {
        for (var i=0; i < data.successful.length; i++) {
            data.successful[i] = log10(data.successful[i]);
        }
        for (var i=0; i < data.incomplete.length; i++) {
            data.incomplete[i] = log10(data.incomplete[i]);
        }
        for (var i=0; i < data.failed.length; i++) {
            data.failed[i] = log10(data.failed[i]);
        }
    }
    if (orientation != 'column') {
        document.getElementById(id).style.height = n * 30;
    }
    plot = new Highcharts.Chart({
        chart: {
            renderTo: id,
            defaultSeriesType: orientation
        },
        title: {
            text: ''
        },
        credits: {
            enabled: false
        },
        tooltip: {
            formatter: function() {
                if (max > 25) {
                    return this.series.name + ': ' + Math.round(Math.pow(10,this.point.y));
                } else {
                    return this.series.name + ': ' + this.point.y;
                }
            }
        },
        xAxis: {
            categories: data.names
        },
        yAxis: {
            min:0,
            title: {
                text: ''
           },
           labels: {
                formatter: function() {
                    if (max > 25) {
                        return Math.round(Math.pow(10, this.value));
                    } else {
                        return this.value;
                    }
                }
            }
        }, 
        legend: {
            backgroundColor: '#FFFFFF',
            reversed: true
        },
        plotOptions: {
            area: {
                shadow: false
            },
            bar: {
                borderWidth: 0
            },
            column: {
                borderWidth: 0
            },
            series: {
                stacking: 'normal',
                animation: false,
            }
        },
        colors: [
            'rgba(0, 200, 0, 0.8)',
            'rgba(200, 200, 0, 0.8)',
            'rgba(255, 0, 0, 0.8)'
        ],
        series: [
        {
            name: 'Successful',
            data: data.successful
        },
        {
            name: 'Incomplete',
            data: data.incomplete
        },
        {
            name: 'Failed',
            data: data.failed
        }]
    });
}

show_subworkflow_info = function(category, uuid) {
    set_sub_uuid(uuid);
    $('#sep3').html("&nbsp;->&nbsp;");
    $('#subworkflow').html('sub-workflow ' + category);
    show_subworkflow_view(uuid, true);
}

show_root_view = function(changeXface) {
    if (changeXface) {
        $('#rootContainer').show();
        $('#subContainer').hide();
        $('#subworkflow_view').val('');
        $('#workflow_view').val('');
        $('#root_view').val('set');
        $('#summaryChartEmpty').show();
        for (i=0; i < 4; i++) {
            $('#summaryChartScroll' + i).hide();
        }
        $("#accordion_wf").accordion({
            active: false 
        });
        $("#accordion_xform").accordion({
             active: false
        });
        $('#accordion_xform').hide();
        $('#accordion_wf_title').html('Select a workflow <span id="selectWorkflow">[?]</span>');
        $("#subcontrols").hide();
    }
    for (i=0; i < 4; i++) {
        $('#summaryChartScroll' + i).empty();
    }
    $('#xformChartScroll').empty();
    $('#rootTable').flexReload({url: '/wf/list'});
}

show_workflow_view = function(changeXface) {
    if (changeXface) {
        $('#subworkflow_view').val('');
        $('#workflow_view').val('set');
        $('#root_view').val('');
        $('#rootContainer').show();
        $('#subContainer').hide();
        // doesn't seem to cause problems if not open
        $('#selectWorkflowHelp').dialog('close');
        $('#selectSubWorkflowHelp').dialog('close');
        $('#accordion_wf_title').html('Summary for workflow ' + $('#dax_label').html() + '<span id="summaryWorkflow"> [?]</span>');
        var active = $("#accordion_wf").accordion("option", "active");
        if (active === false) {
            $("#accordion_wf").accordion({
                active: 0
            });
        }
        $('#summaryChartEmpty').hide();
        for (i=0; i < 4; i++) {
            $('#summaryChartScroll' + i).show();
        }
        $('#accordion_xform').show();
        var active = $("#accordion_xform").accordion("option", "active");
        if (active === false) {
            $("#accordion_xform").accordion({
                active: 0
            });
        }
    }
    $.ajax({
        url: get_info_url(get_uuid()),
        dataType: 'json',
        data: "",
        success: show_summary_stats
    });
}

show_subworkflow_view = function(uuid, changeXface) {
    if (changeXface) {
        $('#subworkflow_view').val('set');
        $('#workflow_view').val('');
        $('#root_view').val('');
        $('#rootContainer').hide();
        $('#subContainer').show();
        $("#subcontrols").hide();
        $('#selectWorkflowHelp').dialog('close');
        $('#selectSubWorkflowHelp').dialog('close');
        $('#subtotals').prop('checked', false);
        $('#accordion_wf_title').html('Summary for sub-workflow ' + '<span id="summaryWorkflow">[?]</span>');
        var active = $("#accordion_wf").accordion("option", "active");
        if (active === false) {
            $("#accordion_wf").accordion({
                active: 0
            });
        }
        $('#summaryChartEmpty').hide();
        for (i=0; i < 4; i++) {
            $('#summaryChartScroll' + i).empty();
            $('#summaryChartScroll' + i).show();
        }
        $('#accordion_xform').show();
        var active = $("#accordion_xform").accordion("option", "active");
        if (active === false) {
            $("#accordion_xform").accordion({
                active: 0
            });
        }
    } else {
        for (i=0; i < 4; i++) {
            $('#summaryChartScroll' + i).empty();
        }
    }
    $.ajax({
        url: get_info_url(uuid),
        dataType: 'json',
        data: "",
        success: show_summary_stats
    });
}

get_info_url = function(uuid) {
    if ($('#subtotals').is(':checked')) {
        return "/wf/" + uuid + "/subinfo";
    } else {
        return "/wf/" + uuid + "/info";
    }
}
