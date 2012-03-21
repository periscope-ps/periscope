// JavaScript for Stampede workflow analyzer.

$(function() {
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
        $('#rootTable').flexReload({url: '/wf/list'});
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
        $('#rootContainer').show();
        $('#subContainer').hide();
        $('#summaryChartScroll').empty();
        $('#xformChartScroll').empty();
        $('#summaryChartEmpty').show();
        $('#summaryChartScroll').hide();
        $("#accordion_wf").accordion({
            active: false 
        });
        $("#accordion_xform").accordion({
             active: false
        });
        $('#accordion_xform').hide();
        $('#accordion_wf_title').html('Select a workflow');
        $("#subcontrols").hide();
        $('#rootTable').flexReload({url: '/wf/list'});
    });
    $('#workflow').click(function() {
        $('#rootContainer').show();
        $('#subContainer').hide();
        $('#accordion_wf_title').html('Summary for workflow ' + $('#dax_label').html());
        var active = $("#accordion_wf").accordion("option", "active");
        if (active === false) {
            $("#accordion_wf").accordion({
                active: 0
            });
        }
        $('#summaryChartEmpty').hide();
        $('#summaryChartScroll').show();
        $('#accordion_xform').show();
        var active = $("#accordion_xform").accordion("option", "active");
        if (active === false) {
            $("#accordion_xform").accordion({
                active: 0
            });
        }
        $.ajax({
            url: get_info_url(get_uuid()),
            dataType: 'json',
            data: "",
            success: show_summary_stats
        });
    });
    $('#subworkflow').click(function() {
        $('#rootContainer').hide();
        $('#subContainer').show();
        $('#accordion_wf_title').html('Summary for sub-workflow ');
        var active = $("#accordion_wf").accordion("option", "active");
        if (active === false) {
            $("#accordion_wf").accordion({
                active: 0
            });
        }
        $('#summaryChartEmpty').hide();
        $('#summaryChartScroll').show();
        $('#accordion_xform').show();
        var active = $("#accordion_xform").accordion("option", "active");
        if (active === false) {
            $("#accordion_xform").accordion({
                active: 0
            });
        }
        $.ajax({
            url: get_info_url(get_sub_uuid()),
            dataType: 'json',
            data: "",
            success: show_summary_stats
        });
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
        $('#summaryChartScroll').empty();
        $('#xformChartScroll').empty();
        $.ajax({
            url: get_info_url(get_uuid()),
            dataType: 'json',
            data: "",
            success: show_summary_stats
        });
    });
});

var summaryChartScroll;
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
            $('#accordion_wf_title').html('Summary for workflow ' + dax_label);
            var active = $("#accordion_wf").accordion("option", "active");
            if (active === false) {
                $("#accordion_wf").accordion({
                    active: 0
                });
            }
            $('#summaryChartEmpty').hide();
            $('#summaryChartScroll').show();
            $('#accordion_xform').show();
            var active = $("#accordion_xform").accordion("option", "active");
            if (active === false) {
                $("#accordion_xform").accordion({
                    active: 0
                });
            }
            $.ajax({
                url: get_info_url(wf_uuid),
                dataType: 'json',
                data: "",
                success: show_summary_stats
            });
        }
    );
}

// Show job, task, transformation, and sub-workflow bars, and get data for
// transformations accordion
show_summary_stats = function(data, text_status, jqxhr) {
    plotScroll(data.summary, 'summaryChartScroll', 'bar', false);
    numSubworkflows = data.summary.successful[3];
    numSubworkflows += data.summary.failed[3];
    numSubworkflows += data.summary.incomplete[3];
    if (numSubworkflows > 0) {
        $("#subcontrols").show();
    }
    plotScroll(data.xforms, 'xformChartScroll', 'bar', false);
}

show_transformations = function(data, text_status, jqxhr) {
    plotScroll(data, 'xformChartScroll', 'bar', false);
}

show_subworkflows = function(data, text_status, jqxhr) {
    $('#rootContainer').hide();
    $('#subContainer').show();
    $('#accordion_wf_title').html('Select a sub-workflow');
    $("#accordion_wf").accordion({
        active: false 
    });
    $("#subcontrols").hide();
    $('#accordion_xform').hide()
    $("#accordion_xform").accordion({
         active: false
    });
    $('#summaryChartScroll').empty();
    $('#xformChartScroll').empty();
    plotScroll(data, 'subChartScroll', 'column', true);
    return;
}

plotScroll = function(data, id, orientation, handleClick) {
    if (id == 'summaryChartScroll') {
        var plot = summaryChartScroll;
    } else if (id == 'xformChartScroll') {
        var plot = xformChartScroll;
    } else if (id == 'subChartScroll') {
        var plot = subChartScroll;
    }
    var jobstate = ['Success','Incomplete','Failure'];
    $('#' + id).empty();
    var n = data.num; // number of bars
    if (orientation != 'column') {
        document.getElementById(id).style.height = n * 40;
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

show_subworkflow_info = function(category, uuid) {
    set_sub_uuid(uuid);
    $('#sep2').html("&nbsp;->&nbsp;");
    $('#subworkflow').html('sub-workflow ' + category);
    $('#accordion_wf_title').html('Summary for sub-workflow ');
    var active = $("#accordion_wf").accordion("option", "active");
    if (active === false) {
        $("#accordion_wf").accordion({
            active: 0
        });
    }
    $('#summaryChartEmpty').hide();
    $('#summaryChartScroll').show();
    $('#accordion_xform').show();
    var active = $("#accordion_xform").accordion("option", "active");
    if (active === false) {
        $("#accordion_xform").accordion({
            active: 0
        });
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

// Refresh table
refresh = function() {
    $.ajax({
        url: "/workflows/",
        dataType: 'json',
        data: "",
        success: show_success
    });
}
