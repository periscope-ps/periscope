/* This function creates a details view table with column 1 as the header and column 2 as the details
 * Parameter Information
 * @param objArray  Anytype of object array, like JSON results
 * @param theme (optional)  A css class to add to the table (e.g. <table class="<theme>">
 * @param enableHeader (optional)  Controls if you want to hide/show, default is show
 */
function createTableView(objArray, theme, enableHeader) {
  // set optional theme parameter
  if (theme === undefined) {
    theme = 'mediumTable'; //default theme
  }

  if (enableHeader === undefined) {
    enableHeader = true; //default enable headers
  }

  // If the returned data is an object do nothing, else try to parse
  var array = typeof objArray != 'object' ? JSON.parse(objArray) : objArray;
  
  var str = '<table border="1" class="' + theme + '">';

  // table head
  if (enableHeader) {
    str += '<thead><tr>';
    for (var i in array) {
      str += '<th scope="col">' + i + '</th>';
    }
    str += '</tr></thead>';
  }

  // table body
  str += '<tbody>';
  str += (i % 2 == 0) ? '<tr class="alt">' : '<tr>';
  for (var index in array) {
    str += '<td>' + array[index] + '</td>';
  }
  str += '</tr>';
  str += '</tbody>'
  str += '</table>';
  return str;
}

function toggleSource(spd){
  if(typeof spd == undefined)
    var spd = null;
  var source = $('input:radio[name=source]:checked').val();
  if(source == "remote"){
    $('#aveDur').hide(spd);
    $('#runningJobs').hide(spd);
    $('#intervalDiv').hide(spd);
    $('#barPlotDiv').hide(spd);
    $('#durHisDiv').hide(spd);
    $('#runHisDiv').hide(spd);

    $('#searchDiv').show(spd);
    $('#workflowTimeSeries').show(spd);
    $('#searchResults').show(spd);
    $('#jobsBarPlotDiv').show(spd);
    $('#customPlot').show(spd);
  }else{
    $('#aveDur').show(spd);
    $('#runningJobs').show(spd);
    $('#intervalDiv').show(spd);
    $('#barPlotDiv').show(spd);
    $('#durHisDiv').show(spd);
    $('#runHisDiv').show(spd);

    $('#searchDiv').hide(spd);
    $('#workflowTimeSeries').hide(spd);
    $('#searchResults').hide(spd);
    $('#jobsBarPlotDiv').hide(spd);
    $('#customPlot').hide(spd);
  }
  if (typeof updInterval != "undefined"){
    updInterval = setInterval(update,interval);
  }
}

/*
 * This function plots four figures and keeps them updated.
 * It also displays and updates the average duration.
 * @param interval: plots' update interval in milliseconds. Default is 1 second
 */
function startPlotting(interval){

  $.jqplot.config.enablePlugins = true;

  var successBarOptions = {
    series: [
    {
      color: 'rgba(0, 255, 0, 0.8)'
    },

    {
      color: 'rgba(255, 0, 0, 0.8)'
    },

    {
      color: 'rgba(255, 0, 255, 0.8)'
    },
    ],
    legend: {
      renderer: $.jqplot.EnhancedLegendRenderer,
      show: true,
      labels: ['Successful', 'Failed', 'Running'],
      rendererOptions:{
        numberRows: 3
      },
      placement: 'insideGrid',
      location: 'ne'
    },
    title: 'Stampede Job Monitor',
    seriesDefaults:{
      renderer: $.jqplot.BarRenderer,
      pointLabels: {
        show: true,
        location: 'n',
        ypadding:0,
        rendererOptions: {
          barDirection: 'horizontal',
          highlightMouseDown: true
        }
      },
      rendererOptions: {
        barPadding: 6,
        barMargin: 20
      }
    },
    axes: {
      xaxis: {
        renderer: $.jqplot.CategoryAxisRenderer,
        ticks: ['Stampede']
      },
      yaxis:{
        //renderer: $.jqplot.CategoryAxisRenderer,
        label: 'Number of Jobs',
        labelRenderer: $.jqplot.CanvasAxisLabelRenderer
      }
    },
    highlighter: {
      show: false
    }

  };

  searchBarOptions = {
    series: [
    {
      color: 'rgba(0, 255, 0, 0.8)'
    },

    {
      color: 'rgba(255, 0, 0, 0.8)'
    }
    ],
    legend: {
      renderer: $.jqplot.EnhancedLegendRenderer,
      show: true,
      labels: ['Successful', 'Failed'],
      rendererOptions:{
        numberRows: 3
      },
      placement: 'insideGrid',
      location: 'ne'
    },
    title: 'Selected Workflow Chart',
    seriesDefaults:{
      renderer: $.jqplot.BarRenderer,
      pointLabels: {
        show: true,
        location: 'n',
        ypadding:0,
        rendererOptions: {
          barDirection: 'horizontal',
          highlightMouseDown: true
        }
      },
      rendererOptions: {
        barPadding: 6,
        barMargin: 20
      }
    },
    axes: {
      xaxis: {
        renderer: $.jqplot.CategoryAxisRenderer,
        ticks: ['Stampede']
      },
      yaxis:{
        //renderer: $.jqplot.CategoryAxisRenderer,
        label: 'Number of Jobs',
        labelRenderer: $.jqplot.CanvasAxisLabelRenderer
      }
    },
    highlighter: {
      show: false
    }

  };

  jobsSuccessBarOptions = {
    series: [
    {
      color: 'rgba(0, 255, 0, 0.8)'
    },

    {
      color: 'rgba(255, 0, 0, 0.8)'
    },
    ],
    legend: {
      renderer: $.jqplot.EnhancedLegendRenderer,
      show: true,
      labels: ['Successful', 'Failed'],
      rendererOptions:{
        numberRows: 3
      },
      placement: 'insideGrid',
      location: 'ne'
    },
    title: 'Stampede Job Monitor',
    seriesDefaults:{
      renderer: $.jqplot.BarRenderer,
      pointLabels: {
        show: true,
        location: 'n',
        ypadding:0,
        rendererOptions: {
          barDirection: 'horizontal',
          highlightMouseDown: true
        }
      },
      rendererOptions: {
        barPadding: 6,
        barMargin: 20
      }
    },
    axes: {
      xaxis: {
        renderer: $.jqplot.CategoryAxisRenderer,
        ticks: ["unknown", "compute","stage_in_tx","stage_out_tx","registration","inter_site_tx","create_dir","staged_compute","cleanup","chmod","dax","dag"]
      },
      yaxis:{
        //renderer: $.jqplot.CategoryAxisRenderer,
        label: 'Number of Jobs',
        labelRenderer: $.jqplot.CanvasAxisLabelRenderer
      }
    },
    highlighter: {
      show: false
    }

  };
  interval = Math.min($('#interval').val(),2500);
    
  updInterval = setInterval(update,interval);
  function update(){ // Updating the graph every [interval]
    clearInterval(updInterval);

    // Start: This resets the graphs when the database source is changed.
    if( typeof db != "undefined"){
      if (db != $('input:radio[name=source]:checked').val()){
            
        delete averageDurationLine;  
        delete loadLine; 
        delete sucLine;
        delete failLine;
      }
    }// End: This resets the graphs when the database source is changed.
    
    // Check what database connection is checked.
    db = $('input:radio[name=source]:checked').val()
    //    console.log("input db: "+db);

    if(db == "local"){
      scriptExec = "getResultsInJSON.py";

      // Load the json file, prevent its caching, and pass the db choice to it.
      $.ajax({
        cache: false,
        url: "cgi-bin/"+scriptExec,
        dataType: "json",
        success: function(data){
          try{
            obj = eval(data);
          }catch(e){
            console.log("Error" + e.toString());
            $.error("Some error occured.");
          }


          // @TODO: refactor the following code.

          /* Parses the data loaded from getResultsInJSON.py,
           * and returns an array of results.
           *      The results array to be returned is of size 4:
           *          results[0]: # of jobs started (obsolete)
           *          results[1]: # of 'success' ended jobs
           *          results[2]: # of 'failure' ended jobs
           *          results[3]: # of still running jobs
           *          results[4]: # of Average Duration (main)
           *          results[5]: Timestamp of the event
           */
          var results = [];

          results[1] = obj.Successful;
          results[2] = obj.Failure;
          results[3] = obj.Running;
          results[4] = obj.MainDuration;
          results[5] = obj.Timestamp;

          $('#runningJobs').text("Running jobs: "+results[3]);
          $('#aveDur').text("Average Duration: " + results[4] + " seconds.");

          // The arrays that'll be plotted.
          var success = [];
          success[0]=results[1];
          var failure = [];
          failure[0]=results[2];
          var running = [];
          running[0]=results[3];

          // Check if the plot has already been initialized.
          if(typeof plot === 'undefined'){ // First time.
            plot = $.jqplot('barPlot', [ success, failure, running],successBarOptions );
          }else{ // The plot alread exists. Replot it.
            plot.series[0].data[0][1]=success[0];
            plot.series[1].data[0][1]=failure[0];
            plot.series[2].data[0][1]=running[0];
            plot.replot({
              resetAxes:true,
              axesDefaults: {
                showTicks: true
              },
              axes:{
                yaxis:{
                  min:0
                }
              },
              seriesDefaults:{
                showMarker: true
              }
            });
          }

          /*
           * Average duration plot start
           */
          if(typeof averageDurationLine == 'undefined')
            averageDurationLine=[];
          averageDurationLine.push([(new Date(1000*results[5])),results[4]]);
          durOptions = {
            seriesDefaults:{
              pointLabels:{
                show:false
              }
            },
            title:'Average duration history',
            axes:{
              xaxis:{
                renderer:$.jqplot.DateAxisRenderer,
                rendererOptions:{
                  tickRenderer:$.jqplot.CanvasAxisTickRenderer
                },
                tickOptions:{
                  formatString:'%X',
                  fontSize:'10pt',
                  fontFamily:'Tahoma',
                  angle:-90,
                  fontWeight:'normal',
                  fontStretch:1
                }
              },
              resetAxis:true
            },
            series:[{
              lineWidth:1,
              markerOptions:{
                style:'plus',
                show:false
              },
              tickOptions:{
                showLabel: false
              }
            }]
          }

          if(typeof durPlot != 'undefined'){
            durPlot.destroy(); // Free it.
            delete durPlot;
            $('#durationLine').html("");
          }
          if($('#durationLine').is(':visible'))
            durPlot = $.jqplot('durationLine', [averageDurationLine],durOptions); // Plot it.
          /*
           * Average duration plot end
           */


          /*
           * Running jobs plot start
           */
          if(typeof loadLine == 'undefined')
            loadLine=[];
          if(typeof sucLine == 'undefined')
            sucLine=[];
          if(typeof failLine == 'undefined')
            failLine=[];

          sucLine.push([new Date(1000*results[5]),results[1]]);
          failLine.push([new Date(1000*results[5]),results[2]]);
          loadLine.push([new Date(1000*results[5]),results[3]]);


          loadOptions = {
            seriesDefaults:{
              pointLabels:{
                show:false
              }
            },
            title:'Load history (number of running jobs)',
            axes:{
              xaxis:{
                renderer:$.jqplot.DateAxisRenderer,
                rendererOptions:{
                  tickRenderer:$.jqplot.CanvasAxisTickRenderer
                },
                tickOptions:{
                  formatString:'%X',
                  fontSize:'10pt',
                  fontFamily:'Tahoma',
                  angle:-90,
                  fontWeight:'normal',
                  fontStretch:1
                }
              },
              resetAxis:true
            },
            series:[{
              lineWidth:1,
              markerOptions:{
                style:'plus',
                show:false
              },
              tickOptions:{
                showLabel: false
              }
            },{
              lineWidth:1,
              markerOptions:{
                style:'plus',
                show:false
              },
              tickOptions:{
                showLabel: false
              }
            },{
              lineWidth:1,
              markerOptions:{
                style:'plus',
                show:false
              },
              tickOptions:{
                showLabel: false
              }
            }]
            ,
            legend: {
              renderer: $.jqplot.EnhancedLegendRenderer,
              show: true,
              labels: ['Running', 'Successful','Failed'],
              rendererOptions:{
                numberRows: 1
              },
              placement: 'insideGrid',
              location: 'n'
            }
          }

          if(typeof loadPlot != 'undefined'){
            loadPlot.destroy(); // Free it.
            delete loadPlot;
            $('#runningLine').html("");
          }
          if($('#runningLine').is(':visible'))
            loadPlot = $.jqplot('runningLine', [loadLine , sucLine, failLine],loadOptions); // Plot it.
          /*
           * Running jobs plot end
           */

          interval = Math.min($('#interval').val(),2500);
          updInterval = setInterval(update,interval);

        },
        error: function(jqXHR, textStatus, errorThrown){
          console.log("Unsuccessful: " + textStatus);
          console.log(errorThrown.toString());
          update();
        }
      });
    }
    else{
      interval = Math.min($('#interval').val(),2500);
      updInterval = setInterval(update,interval);
    }

  }
}

$(document).ready(function(){
  
  toggleSource();
  $('#getWFs').submit(function(e){
    // Prevent default action.
    e.preventDefault();
    
    dbName = $("#dbName").val();
    $.ajax({
      cache: false,
      url: "cgi-bin/getWfs.py?db_name="+dbName,
      dataType: "json",
      success: function(data){
        $('#searchKey').html("<option>Select Workflow UUID</option>");
        $.each(data, function(key, value){
          $('#searchKey').
          append($("<option></option>").
            attr("value",key).
            text(value));
        });
      }
    })
  })
  $("#searchResults").hide();

  // Handle search.
  $('#search').submit(function(e){
    // Prevent default action.
    e.preventDefault();

    // Get search key
    searchKey = $("#searchKey option:selected").text();
    console.log(dbName);

    dbName = $("#dbName").val();
    if($.trim(searchKey) != "" && $.trim(searchKey) != null ){
      // Call the searchID.py script with searchKey as parameter.
      $.ajax({
        cache: false,// prevent cahcing.
        url: "cgi-bin/searchID.py?key="+searchKey+"&db_name="+dbName,
        dataType: "json",
        success: function(data){
          // Plot the job types bar chart.

          // Check if the plot has already been initialized.
          if(typeof jobsPlot === 'undefined'){ // First time.
            // This following code defines the bar data.
            // Please refer to the jqPlot documentation for elaborated explanation.
            jobsPlot = $.jqplot('jobsBarPlot', [[
              data.type_statistics.unknown.successful,
              data.type_statistics.compute.successful,
              data.type_statistics.stage_in_tx.successful,
              data.type_statistics.stage_out_tx.successful,
              data.type_statistics.registration.successful,
              data.type_statistics.inter_site_tx.successful,
              data.type_statistics.create_dir.successful,
              data.type_statistics.staged_compute.successful,
              data.type_statistics.cleanup.successful,
              data.type_statistics.chmod.successful,
              data.type_statistics.dax.successful,
              data.type_statistics.dag.successful
              ] ,[
              data.type_statistics.unknown.fail,
              data.type_statistics.compute.fail,
              data.type_statistics.stage_in_tx.fail,
              data.type_statistics.stage_out_tx.fail,
              data.type_statistics.registration.fail,
              data.type_statistics.inter_site_tx.fail,
              data.type_statistics.create_dir.fail,
              data.type_statistics.staged_compute.fail,
              data.type_statistics.cleanup.fail,
              data.type_statistics.chmod.fail,
              data.type_statistics.dax.fail,
              data.type_statistics.dag.fail
              ]],jobsSuccessBarOptions );

          }else{ // The plot alread exists. Replot it.
            jobsPlot.series[0].data[0][1]=data.type_statistics.unknown.successful;
            jobsPlot.series[1].data[0][1]=data.type_statistics.unknown.fail;

            jobsPlot.series[0].data[1][1]=data.type_statistics.compute.successful;
            jobsPlot.series[1].data[1][1]=data.type_statistics.compute.fail;

            jobsPlot.series[0].data[2][1]=data.type_statistics.stage_in_tx.successful;
            jobsPlot.series[1].data[2][1]=data.type_statistics.stage_in_tx.fail;

            jobsPlot.series[0].data[3][1]=data.type_statistics.stage_out_tx.successful;
            jobsPlot.series[1].data[3][1]=data.type_statistics.stage_out_tx.fail;

            jobsPlot.series[0].data[4][1]=data.type_statistics.registration.successful;
            jobsPlot.series[1].data[4][1]=data.type_statistics.registration.fail;

            jobsPlot.series[0].data[5][1]=data.type_statistics.inter_site_tx.successful;
            jobsPlot.series[1].data[5][1]=data.type_statistics.inter_site_tx.fail;

            jobsPlot.series[0].data[6][1]=data.type_statistics.create_dir.successful;
            jobsPlot.series[1].data[6][1]=data.type_statistics.create_dir.fail;

            jobsPlot.series[0].data[7][1]=data.type_statistics.staged_compute.successful;
            jobsPlot.series[1].data[7][1]=data.type_statistics.staged_compute.fail;

            jobsPlot.series[0].data[8][1]=data.type_statistics.cleanup.successful;
            jobsPlot.series[1].data[8][1]=data.type_statistics.cleanup.fail;

            jobsPlot.series[0].data[9][1]=data.type_statistics.chmod.successful;
            jobsPlot.series[1].data[9][1]=data.type_statistics.chmod.fail;

            jobsPlot.series[0].data[10][1]=data.type_statistics.dax.successful;
            jobsPlot.series[1].data[10][1]=data.type_statistics.dax.fail;

            jobsPlot.series[0].data[11][1]=data.type_statistics.dag.successful;
            jobsPlot.series[1].data[11][1]=data.type_statistics.dag.fail;

            jobsPlot.replot({
              resetAxes:true,
              axesDefaults: {
                showTicks: true
              },
              axes:{
                yaxis:{
                  min:0
                }
              },
              seriesDefaults:{
                showMarker: true
              }
            });
          }

          // Plot searched workflow's bar chart
          // Check if the plot has already been initialized.
          if(typeof customResultPlot == 'undefined'){ // First time.
            customResultPlot = $.jqplot('customPlot', [ [data.totals.successful], [data.totals.failing]],searchBarOptions );
          }else{ // The customPlot alread exists. Replot it.
            customResultPlot.series[0].data[0][1]=data.totals.successful;
            customResultPlot.series[1].data[0][1]=data.totals.failing;
            customResultPlot.replot({
              resetAxes:true,
              axesDefaults: {
                showTicks: true
              },
              axes:{
                yaxis:{
                  min:0
                }
              },
              seriesDefaults:{
                showMarker: true
              }
            });
            
          }

          var tsdOptions = {
            seriesDefaults:{
              pointLabels:{
                show:false
              }
            },
            title:'Workflow Time Series',
            axes:{
              xaxis:{
                renderer:$.jqplot.DateAxisRenderer,
                rendererOptions:{
                  tickRenderer:$.jqplot.CanvasAxisTickRenderer
                },
                tickOptions:{
                  formatString:'%X',
                  fontSize:'10pt',
                  fontFamily:'Tahoma',
                  angle:-90,
                  fontWeight:'normal',
                  fontStretch:1
                }
              },
              resetAxis:true
            },
            series:[{
              lineWidth:1,
              markerOptions:{
                style:'plus',
                show:false
              },
              tickOptions:{
                showLabel: false
              }
            },{
              lineWidth:1,
              markerOptions:{
                style:'plus',
                show:false
              },
              tickOptions:{
                showLabel: false
              }
            }]
            ,
            legend: {
              renderer: $.jqplot.EnhancedLegendRenderer,
              show: true,
              labels: ['Successful', 'Failure'],
              rendererOptions:{
                numberRows: 1
              },
              placement: 'insideGrid',
              location: 'n'
            }
          }
          var tsdSucc = [];
          var tsdFail = [];
          $.each(data.timeseries_data, function(k, ts) {
            tsdSucc.push([new Date(1000*parseInt(ts.timestamp)),ts.successful]);
            tsdFail.push([new Date(1000*parseInt(ts.timestamp)),ts.fail]);
          })

          if(typeof tsdPlot == 'undefined'){ // First time.
            tsdPlot = $.jqplot('workflowTimeSeries', [tsdSucc, tsdFail],tsdOptions );
          }else{ // The customPlot alread exists. Replot it.
            delete tsdPlot;
//            $('#workflowTimeSeries').html("");
            tsdPlot = $.jqplot('workflowTimeSeries', [tsd],tsdOptions );
          }

          console.log(tsdPlot.series[0]);

          // Formulate the search results as HTML table, and show it.
          $("#searchResults").html(createTableView(data.api_summaries,"resultsTable")).show('slow');


        }
      })
    }
  });

  // Handle the clear button.
  $('#clear').click(function(){
    $("#searchResults").hide("slow").html("");
    if(typeof jobsPlot != 'undefined'){
      delete jobsPlot;
      $("#jobsBarPlot").html("");
    }
    if(typeof customResultPlot != 'undefined'){
      delete customResultPlot;
      $("#customPlot").html("");
    }
    if(typeof tsdPlot != 'undefined'){
      delete tsdPlot;
      $("#workflowTimeSeries").html("");
    }
  })

  // Handle the interval field.
  $('#interval').change(function(){
    clearInterval(updInterval);
    // I defined the maximum value as 2.5 seconds (change it to your convenience)
    interval = Math.min($('#interval').val(),2500);
    updInterval = setInterval(update,interval);
  });

  // Handle db source change.
  $('.dbRadoi').change(function(){
    toggleSource('slow');
  });
  
  // Finally, start plotting the dynamic plots.
  startPlotting($('#interval').val());
})
