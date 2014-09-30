/*
 * Helm Page Controller
 * public/js/controllers/
 * HelmCtrl.js
 */

angular.module('HelmCtrl', []).controller('HelmController', function($scope, $http, Service, Slice) {

  // scope for d3 graph data
  $scope.graphNodes = [];
  $scope.graphLinks = [];
  $scope.ports = [];
  $scope.selectedPortMap = {};
  $scope.selectedPortSourceId = "";
  // scope variables
  $scope.helmIperfData = {};
  $scope.helmPingData = {};
  $scope.alerts = [];
  $scope.timeTypes = [
    {type:'Seconds'},
    {type:'Minutes'},
    {type:'Hours'},
    {type:'Days'}
  ];
  $scope.bandTesters = [
    {type:'Iperf'}
  ];
  $scope.protos = [
    {type:'tcp'},
    {type:'udp'}
  ];
  
  $scope.selectPortD = function(st,end,e){	  
	  var port = this.port ;
	  this.Links.selectedPort = this.$index;
	  this.selectedPortMap[st+"#"+end] = port ;
  };	
  $scope.selectPort = function(st,end){	  
	  var port = this.port ;
	  var id = this.ports.selectedPortSourceId;
	  //this.graphLinks.selectedPort = 3;
	  this.selectedPortMap[id] = port ;
   };	
  Slice.getSlice(function(sliceInfo) {
    $scope.geniSlice = sliceInfo[0];
  });
  Service.getServices(function(services) {
    $scope.services = services;
  });

  // alerts for this scope
  $scope.addAlert = function(msg, type) {
    $scope.alerts.push({type: type, msg: msg});
  };
  $scope.closeAlert = function(index) {
    $scope.alerts.splice(index, 1);
  };

  // load default form data, toggle ui buttons
  $scope.togglePing = function() {
    $scope.addIperf = false;
    $scope.btnIperf = "btn btn-default";
    $scope.btnPing = $scope.btnPing === "btn btn-primary active" ? "btn btn-default": "btn btn-primary active";
    $scope.addPing = $scope.addPing === true ? false: true;

    $scope.helmPing = angular.copy({});
    $scope.helmPing.num_tests = 1;
    $scope.helmPing.tbtValue = 5;
    $scope.helmPing.tbtType = $scope.timeTypes[1];
    $scope.helmPing.packetsSent = 1;
    $scope.helmPing.tbp = 1;
    $scope.helmPing.packetSize = 1000;
    $scope.helmPing.reportMS = 10;
    $scope.alert = false;
  };
  $scope.toggleIperf = function() {
    $scope.addPing = false;
    $scope.btnPing = "btn btn-default";
    $scope.btnIperf = $scope.btnIperf === "btn btn-primary active" ? "btn btn-default": "btn btn-primary active";
    $scope.addIperf = $scope.addIperf === true ? false: true;

    // default form values
    $scope.helmIperf = angular.copy({});
    $scope.helmIperf.num_tests = 1;
    $scope.helmIperf.tbtValue = 4;
    $scope.helmIperf.tbtType = $scope.timeTypes[1];
    $scope.helmIperf.td = 20;
    $scope.helmIperf.bt = $scope.bandTesters[0];
    $scope.helmIperf.proto = $scope.protos[0];
    $scope.alert = false;
  };

  // reset forms to default values we recommend
  $scope.helmReset = function() {
    // clear client and server side form
    // $scope.helmData = {};
    // $scope.helm = angular.copy($scope.helmData);
    if ($scope.addIperf === true) {
      // default form values
      $scope.helmIperf = angular.copy({});
      $scope.helmIperf.num_tests = 1;
      $scope.helmIperf.tbtValue = 4;
      $scope.helmIperf.tbtType = $scope.timeTypes[1];
      $scope.helmIperf.td = 20;
      $scope.helmIperf.bt = $scope.bandTesters[0];
      $scope.helmIperf.proto = $scope.protos[0];
    } else if ($scope.addPing === true) {
      // default form values
      $scope.helmPing = angular.copy({});
      $scope.helmPing.num_tests = 1;
      $scope.helmPing.tbtValue = 5;
      $scope.helmPing.tbtType = $scope.timeTypes[1];
      $scope.helmPing.packetsSent = 1;
      $scope.helmPing.tbp = 1;
      $scope.helmPing.packetSize = 1000;
      $scope.helmPing.reportMS = 10;
     } else {
      return;
     }

    $scope.closeAlert(0);
  };

  // compare form data with in memory data
  $scope.helmReset();
  $scope.helmPingUnchanged = function(helmPing) {
    return angular.equals(helmPing, $scope.helmPingData);
  };
  $scope.helmIperfUnchanged = function(helmIperf) {
    return angular.equals(helmIperf, $scope.helmIperfData);
  };
  
  // find the port for a node
  $scope.getNodePort = function(node_ref,portNum) {
	portNum = portNum || 0;
    for(var i = 0; i < $scope.nodes.length; i++) {    	
      if ($scope.nodes[i].selfRef === node_ref) {
    	  if(!$scope.nodes[i].ports[portNum])
    		  // Atleast one port should be present or it is bad data
    		  // Redirect to 0 if incorrect port number given
    		  portNum = 0 ;
    	  
    	  return $scope.nodes[i].ports[portNum].href.replace(/%3A/g, ':');
      }
    }
  };

  // find the port ip
  $scope.getPortIP = function(port_ref) {
    for(var i = 0; i < $scope.ports.length; i++) {
      if ($scope.ports[i].selfRef === port_ref) {
        return $scope.ports[i].properties.geni.ip.address;
      }
    }
  };
  $scope.helmSubmit = function(helmForm) {
    if (helmForm.$invalid) {
      // If form is invalid, return and let AngularJS show validation errors.
      $scope.addAlert('Invalid form, cannot be submitted', 'danger');
      $scope.alert = true;
      return;
    } else {
      // Tell user form has been sent
      // $scope.addAlert('Data sent to UNIS. Please wait for confirmation.', 'info');
      // $scope.alert = true;

      if ($scope.addIperf === true) {
        // copy data submitted by form
        $scope.helmIperfData = angular.copy(helmForm);

        var every;
        if($scope.helmIperfData.tbtType.type === 'Days') {
          every = $scope.helmIperfData.tbtValue * 86400;
        } else if($scope.helmIperfData.tbtType.type === 'Hours') {
          every = $scope.helmIperfData.tbtValue * 3600;
        } else if($scope.helmIperfData.tbtType.type === 'Minutes') {
          every = $scope.helmIperfData.tbtValue * 60;
        } else {
          every = $scope.helmIperfData.tbtValue;
        }
        
        //var nodePort = $scope.getNodePort($scope.helmIperfData.to.split(" ")[1]);
        //var portIP = $scope.getPortIP(nodePort);       
        // build ping command from user options
        if ($scope.helmIperfData.proto.type == 'udp') {
          var perf_command = "iperf -u -c " +" -t " + $scope.helmIperfData.td +  " -y C ";
        } else {
          var perf_command = "iperf -c "+ " -t " + $scope.helmIperfData.td +  " -y C ";
        }

        var from_node, to_node, from_service, to_service, pair;
        var participantLinks = [];

        for(var i = 0; i < $scope.graphLinks.length; i++) {
          pair = $scope.graphLinks[i];
          from_node = $scope.graphNodes[pair[0]][2];
          to_node = $scope.graphNodes[pair[1]][2];

          for(var j = 0; j < $scope.services.length; j++) {
            if($scope.services[j].runningOn.href.split('/')[4] === from_node) {
              from_service = $scope.services[j].selfRef;
            }
            if($scope.services[j].runningOn.href.split("/")[4] === to_node) {
              to_service = $scope.services[j].selfRef;
            }
          }
          var port ;
          try{
        	  port = $scope.selectedPortMap[pair[0]+'#'+pair[1]].href;
          }catch(e){}
          participantLinks.push({from: from_service, to: to_service , port : port});
        }

        var helm_measurement = {
          $schema: "http://unis.incntre.iu.edu/schema/20140214/measurement#",
          ts: Math.round(new Date().getTime() * 1000),
          participants: participantLinks,
          properties: {
            geni: {
              slice_uuid: $scope.geniSlice.slice_uuid
            }
          },
          eventTypes: [
            "ps:tools:helm"
          ],
          configuration: {
            status: "ON",
            regex: ",(?P<bandwidth>\\d+)$",
            window_size: 0,
            protocol: $scope.helmIperfData.proto.type,
            probe_module: "cmd_line_probe",
            test_duration: parseInt($scope.helmIperfData.td),
            schedule_params: {
              every: every,
              num_tests: parseInt($scope.helmIperfData.num_tests)
            },
            tool: "iperf",
            reporting_params: 1,
            client: null,
            command: perf_command,
            ms_url: $scope.geniSlice.ms_url,
            eventTypes: {
              bandwidth: "ps:tools:blipp:linux:net:iperf:bandwidth"
            },
            udp_bandwidth: 0,
            collection_schedule: "builtins.simple",
            name: $scope.helmIperfData.desc
          },
          type: "iperf"
        };
      } else if ($scope.addPing === true) {
        // copy data submitted by form
        $scope.helmPingData = angular.copy(helmForm);

        var every;
        if($scope.helmPingData.tbtType.type === 'Days') {
          every = $scope.helmPingData.tbtValue * 86400;
        } else if($scope.helmPingData.tbtType.type === 'Hours') {
          every = $scope.helmPingData.tbtValue * 3600;
        } else if($scope.helmPingData.tbtType.type === 'Minutes') {
          every = $scope.helmPingData.tbtValue * 60;
        } else {
          every = $scope.helmPingData.tbtValue;
        }

        // lookup port running on given node
        //var nodePort = $scope.getNodePort($scope.pingData.to.split(" ")[1]);
        //var portIP = $scope.getPortIP(nodePort);
        // build ping command from user options
        var ping_command = "ping -c 1 -s " + $scope.helmPingData.packetSize + " -i " + $scope.helmPingData.tbp ;

        var from_node, to_node, from_service, to_service, pair;
        var participantLinks = [];

        for(var i = 0; i < $scope.graphLinks.length; i++) {
          pair = $scope.graphLinks[i];
          from_node = $scope.graphNodes[pair[0]][2];
          to_node = $scope.graphNodes[pair[1]][2];
          for(var j = 0; j < $scope.services.length; j++) {
            if($scope.services[j].runningOn.href.split('/')[4] === from_node) {
              from_service = $scope.services[j].selfRef;
            }
            if($scope.services[j].runningOn.href.split("/")[4] === to_node) {
              to_service = $scope.services[j].selfRef;
            }
          }          
          var port ;
          try{
        	  port = $scope.selectedPortMap[pair[0]+'#'+pair[1]].href;
          }catch(e){}
          
          participantLinks.push({from: from_service, to: to_service , port : port });
        }

        // build ping measurement to submit
        var helm_measurement = {
          $schema: "http://unis.incntre.iu.edu/schema/20140214/measurement#",
          ts: Math.round(new Date().getTime() * 1000),
          participants: participantLinks,
          properties: {
            geni: {
              slice_uuid: $scope.geniSlice.slice_uuid
            }
          },
          eventTypes: [
            "ps:tools:helm"
          ],
          configuration: {
            status: "ON",
            regex: "ttl=(?P<ttl>\\d+).*time=(?P<rtt>\\d+\\.\\d+|\\d+)",
            reporting_params: parseInt($scope.helmPingData.reportMS),
            probe_module: "cmd_line_probe",
            packet_interval: parseInt($scope.helmPingData.tbp),
            collection_schedule: "builtins.simple",
            packet_size: parseInt($scope.helmPingData.packetSize),
            packet_count: 1,
            command: ping_command,
            schedule_params: {
              every: every,
              num_tests: parseInt($scope.helmIperfData.num_tests)
            },
            collection_size: 100000,
            ms_url: $scope.geniSlice.ms_url,
            eventTypes: {
              rtt: "ps:tools:blipp:linux:net:ping:rtt",
              ttl: "ps:tools:blipp:linux:net:ping:ttl"
            },
            collection_ttl: 1500000,
            name: $scope.helmPingData.desc
          },
          type: "ping"
        };
      } else {
        return;
      }

      $http({
        method: 'POST',
        url: '/api/measurements',
        data: helm_measurement,
        headers: {'Content-type': 'application/perfsonar+json'}
      }).
      success(function(data, status, headers, config) {
        // $scope.addAlert(data, 'success');
        // $scope.addAlert(status, 'success');
        // $scope.addAlert(headers, 'success');
        // $scope.addAlert(config, 'success');
        $scope.addAlert('HELM Test: ' + data.configuration.name + ' submitted to UNIS', 'success');
        $scope.alert = true;
      }).
      error(function(data, status, headers, config) {
        // $scope.addAlert(data, 'danger');
        // $scope.addAlert(status, 'danger');
        // $scope.addAlert(headers, 'danger');
        // $scope.addAlert(config, 'danger');
        $scope.addAlert('Status: ' + status.toString() + ', ' + 'Error: ' + data.error.message, 'danger');
        $scope.alert = true;
      });
    }
  }; // end helm submit
}); // end controller
