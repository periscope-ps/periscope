/*
 * Blipp Page Controller
 * public/js/controllers/
 * BlippCtrl.js
 */

angular.module('BlippCtrl', []).controller('BlippController', function($scope, $http, Node, Slice, Service, Port) {

  $scope.userSchema = "";
  $scope.schema = {};

  /*$scope.userSchema = {
    "$schema": "http://json-schema.org/draft-03/hyper-schema#",
    "id": "http://unis.incntre.iu.edu/schema/20140214/measurement#",
    "description": "A measurement object",
    "name": "Measurement",
    "type": "object",
    "extends": {
      "$ref": "http://unis.incntre.iu.edu/schema/20140214/networkresource#"
    },
    "properties": {
      "service": {
        "type": "string",
        "format": "uri",
        "description": "Service which will be taking this measurement"
      },
      "configuration": {
        "type": "object",
        "properties": {
          "$schema": {
            "type": "string",
            "format": "uri"
          }
        },
        "additionalProperties": true
      },
      "scheduled_times": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "start": {
              "type": "string",
              "format": "date-time"
            },
            "end": {
              "type": "string",
              "format": "date-time"
            }
          },
          "required": ["start", "end"]
        }
      },
      "eventTypes": {
        "description": "A list of eventTypes which this measurement produces",
        "type": "array",
        "items": {
          "type": "string"
        }
      },
      "resources": {
        "description": "A list of resources that this measurement uses or affects",
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "ref": {
              "description": "Hyperlink reference to the resource",
              "format": "uri",
              "type": "string"
            },
            "usage": {
              "type": "object",
              "description": "A resource has different ways it can be used, this tells in what ways this measurement uses this resource",
              "additionalProperties": {
                "type": "number",
                "minimum": 0,
                "maximum": 100
              }
            }
          },
          "required": ["ref"]
        }
      }
    },
    "required": [
      "service",
      "configuration",
      "eventTypes"
    ],
    "additionalProperties": true
  };*/

  $scope.userSchemaSubmit = function(userSchema) {
    // userSchema = userSchema.replace(/[$_a-zA-Z]+:(?!\/)/g, '"pants":');
    var schema = angular.copy(userSchema);
    $scope.schema = angular.fromJson(schema);

    $scope.form = [
      // "service",
      "configuration",
      "scheduled_times",
      {
        "key": "eventTypes",
        "type": "array"
      },
      {
        "key": "resources",
        "items": [
          "resources[].ref"
          // "resources[].usage.additionalProperties"
        ]
      },
      {
        "type": "submit",
        "style": "btn-primary",
        "title": "Submit Custom Probe"
      }
    ];

    $scope.model = {};

    $scope.schemaSubmit = function() {

      if ($scope.model == null) {
        // If form is invalid, return and let AngularJS show validation errors.
        $scope.addAlert('Invalid form, cannot be submitted', 'danger');
        $scope.alert = true;
        return;
      } else {
        // Tell user form has been sent
        // $scope.addAlert('Data sent to UNIS. Please wait for confirmation.', 'info');
        // $scope.alert = true;

        // lookup service running on given node
        var nodeService = $scope.getNodeService($scope.model.from.split(" ")[1]);

        // create proper interval for every based on user input
        var every;
        if($scope.model.tbtType.type === 'Days') {
          every = $scope.model.tbtValue * 86400;
        } else if($scope.model.tbtType.type === 'Hours') {
          every = $scope.model.tbtValue * 3600;
        } else if($scope.model.tbtType.type === 'Minutes') {
          every = $scope.model.tbtValue * 60;
        } else {
          every = $scope.model.tbtValue;
        }

        // build schema measurement to submit
        var schema_measurement = {
          $schema: "http://unis.incntre.iu.edu/schema/20140214/measurement#",
          name: "Measurement",
          description: $scope.model.desc,
          service: nodeService,
          ts: Math.round(new Date().getTime() * 1000),
          properties: {
            geni: {
              slice_uuid: $scope.geniSlice.slice_uuid
            }
          },
          eventTypes: $scope.model.eventTypes,
          configuration: {
            status: "ON",
            ref: $scope.model.resources[0].ref,
            command: $scope.model.configuration.$schema,
            // regex: "ttl=(?P<ttl>\\d+).*time=(?P<rtt>\\d+\\.\\d+|\\d+)",
            // reporting_params: parseInt($scope.pingData.reportMS),
            probe_module: "cmd_line_probe",
            collection_schedule: "builtins.simple",
            schedule_params: {
              every: every,
              num_tests: parseInt($scope.model.num_tests),
              start: $scope.model.scheduled_times[0].start,
              end: $scope.model.scheduled_times[0].end
            },
            collection_size: 100000,
            ms_url: $scope.geniSlice.ms_url,
            collection_ttl: 1500000,
          },
          type: "custom_probe"
        };

        $http({
          method: 'POST',
          url: '/api/measurements',
          data: schema_measurement,
          headers: {'Content-type': 'application/perfsonar+json'}
        }).
        success(function(data, status, headers, config) {
          // $scope.addAlert(data, 'success');
          // $scope.addAlert(status, 'success');
          // $scope.addAlert(headers, 'success');
          // $scope.addAlert(config, 'success');
          $scope.addAlert('BLiPP Test: ' + data.configuration.name + ' submitted to UNIS', 'success');
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
    }
  };

  // scope variables
  $scope.pingData = {};
  $scope.owpData = {};
  $scope.perfData = {};
  $scope.netlogData = {};
  $scope.userSchemaData = {};
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

  // load default form
  // $scope.btnIperf = $scope.btnIperf === "btn btn-primary active" ? "btn btn-default": "btn btn-primary active";
  // $scope.addIperf = $scope.addIperf === true ? false: true;
  $scope.btnCustomProbe = $scope.btnCustomProbe === "btn btn-primary active" ? "btn btn-default": "btn btn-primary active";
  $scope.addCustomProbe = $scope.addCustomProbe === true ? false: true;

  // load dependent data
  Node.getNodes(function(nodes) {
    $scope.nodes = nodes;
  });
  Slice.getSlice(function(sliceInfo) {
    $scope.geniSlice = sliceInfo[0];
  });
  Service.getServices(function(services) {
    $scope.services = services;
  });
  Port.getPorts(function(ports) {
    $scope.ports = ports;
  });

  // global node shouldn't be selectable
  $scope.filterNodes = function(node) {
    if(node.name != 'GN0')
    {
      return true;
    }
    return false;
  };

  // find the service running on a node
  $scope.getNodeService = function(node_ref) {
    alert("start");
    for(var i = 0; i < $scope.services.length; i++) {
      if ($scope.services[i].runningOn.href == node_ref) {
        alert("if");
        return $scope.services[i].selfRef;
      } else {
        alert("else");
        return node_ref;
      }
    }
  };

  // find the port for a node
  $scope.getNodePort = function(node_ref) {
    for(var i = 0; i < $scope.nodes.length; i++) {
      if ($scope.nodes[i].selfRef === node_ref) {
        return $scope.nodes[i].ports[0].href.replace(/%3A/g, ':');
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

  // alerts for this scope
  $scope.addAlert = function(msg, type) {
    $scope.alerts.push({type: type, msg: msg});
  };
  $scope.closeAlert = function(index) {
    $scope.alerts.splice(index, 1);
  };

  // load default form data, toggle ui buttons
  $scope.togglePing = function() {
    $scope.addOWPing = false;
    $scope.btnOWPing = "btn btn-default";
    $scope.addIperf = false;
    $scope.btnIperf = "btn btn-default";
    $scope.addNetlogger = false;
    $scope.btnNetlogger = "btn btn-default";
    $scope.addCustomProbe = false;
    $scope.btnCustomProbe = "btn btn-default";
    $scope.btnPing = $scope.btnPing === "btn btn-primary active" ? "btn btn-default": "btn btn-primary active";
    $scope.addPing = $scope.addPing === true ? false: true;

    // default form values
    $scope.ping = angular.copy({});
    $scope.ping.num_tests = 1;
    $scope.ping.tbtValue = 5;
    $scope.ping.tbtType = $scope.timeTypes[1];
    $scope.ping.packetsSent = 1;
    $scope.ping.tbp = 1;
    $scope.ping.packetSize = 1000;
    $scope.ping.reportMS = 10;
    $scope.alert = false;
  };
  /*$scope.toggleOWPing = function() {
    $scope.addPing = false;
    $scope.btnPing = "btn btn-default";
    $scope.addIperf = false;
    $scope.btnIperf = "btn btn-default";
    $scope.addNetlogger = false;
    $scope.btnNetlogger = "btn btn-default";
    $scope.addCustomProbe = false;
    $scope.btnCustomProbe = "btn btn-default";
    $scope.btnOWPing = $scope.btnOWPing === "btn btn-primary active" ? "btn btn-default": "btn btn-primary active";
    $scope.addOWPing = $scope.addOWPing === true ? false: true;

    // default form values
    // $scope.ping.tbtValue = 5;
    // $scope.ping.tbtType = $scope.timeTypes[1];
    // $scope.ping.packetsSent = 1;
    // $scope.ping.tbp = 1;
    // $scope.ping.packetSize = 1000;
    // $scope.ping.reportMS = 10;
    // $scope.alert = false;
  };*/
  $scope.toggleIperf = function() {
    $scope.addPing = false;
    $scope.btnPing = "btn btn-default";
    $scope.addOWPing = false;
    $scope.btnOWPing = "btn btn-default";
    $scope.addNetlogger = false;
    $scope.btnNetlogger = "btn btn-default";
    $scope.addCustomProbe = false;
    $scope.btnCustomProbe = "btn btn-default";
    $scope.btnIperf = $scope.btnIperf === "btn btn-primary active" ? "btn btn-default": "btn btn-primary active";
    $scope.addIperf = $scope.addIperf === true ? false: true;

    // default form values
    $scope.perf = angular.copy({});
    $scope.perf.num_tests = 1;
    $scope.perf.tbtValue = 4;
    $scope.perf.tbtType = $scope.timeTypes[2];
    $scope.perf.td = 20;
    $scope.perf.bt = $scope.bandTesters[0];
    $scope.perf.proto = $scope.protos[0];
    $scope.alert = false;
  };
  $scope.toggleNetlogger = function() {
    $scope.addPing = false;
    $scope.btnPing = "btn btn-default";
    $scope.addOWPing = false;
    $scope.btnOWPing = "btn btn-default";
    $scope.addIperf = false;
    $scope.btnIperf = "btn btn-default";
    $scope.addCustomProbe = false;
    $scope.btnCustomProbe = "btn btn-default";
    $scope.btnNetlogger = $scope.btnNetlogger === "btn btn-primary active" ? "btn btn-default": "btn btn-primary active";
    $scope.addNetlogger = $scope.addNetlogger === true ? false: true;

    // default form values
    $scope.netlog = angular.copy({});
    $scope.netlog.num_tests = 1;
    $scope.netlog.tbrValue = 5;
    $scope.netlog.tbrType = $scope.timeTypes[0];
    $scope.netlog.reportMS = 10;
    $scope.alert = false;
  };
  $scope.toggleCustomProbe = function() {
    $scope.addPing = false;
    $scope.btnPing = "btn btn-default";
    $scope.addOWPing = false;
    $scope.btnOWPing = "btn btn-default";
    $scope.addIperf = false;
    $scope.btnIperf = "btn btn-default";
    $scope.addNetlogger = false;
    $scope.btnNetlogger = "btn btn-default";
    $scope.btnCustomProbe = $scope.btnCustomProbe === "btn btn-primary active" ? "btn btn-default": "btn btn-primary active";
    $scope.addCustomProbe = $scope.addCustomProbe === true ? false: true;

    // default form values
    $scope.user_schema = angular.copy({});
    $scope.alert = false;
  };

  // reset forms to default values we recommend
  $scope.pingReset = function() {
    // clear client and server side form
    // $scope.pingData = {};
    // $scope.ping = angular.copy($scope.pingData);

    // clear client side form and reset defaults
    $scope.ping = angular.copy({});
    $scope.ping.num_tests = 1;
    $scope.ping.tbtValue = 5;
    $scope.ping.tbtType = $scope.timeTypes[1];
    $scope.ping.packetsSent = 1;
    $scope.ping.tbp = 1;
    $scope.ping.packetSize = 1000;
    $scope.ping.reportMS = 10;
    $scope.closeAlert(0);
  };
  /*$scope.owpReset = function() {
    // clear client and server side form
    // $scope.pingData = {};
    // $scope.ping = angular.copy($scope.pingData);

    // clear client side form and reset defaults
    // $scope.ping = angular.copy({});
    // $scope.ping.tbtValue = 5;
    // $scope.ping.tbtType = $scope.timeTypes[1];
    // $scope.ping.packetsSent = 1;
    // $scope.ping.tbp = 1;
    // $scope.ping.packetSize = 1000;
    // $scope.ping.reportMS = 10;
    // $scope.closeAlert(0);
  };*/
  $scope.perfReset = function() {
    // clear client and server side form
    // $scope.perfData = {};
    // $scope.perf = angular.copy($scope.perfData);

    // clear client side form and reset defaults
    $scope.perf = angular.copy({});
    $scope.perf.num_tests = 1;
    $scope.perf.tbtValue = 4;
    $scope.perf.tbtType = $scope.timeTypes[2];
    $scope.perf.td = 20;
    $scope.perf.bt = $scope.bandTesters[0];
    $scope.perf.proto = $scope.protos[0];
    $scope.closeAlert(0);
  };
  $scope.netlogReset = function() {
    // clear client and server side form
    // $scope.netlogData = {};
    // $scope.netlog = angular.copy($scope.netlogData);

    // clear client side form and reset defaults
    $scope.netlog = angular.copy({});
    $scope.netlog.num_tests = 1;
    $scope.netlog.tbrValue = 5;
    $scope.netlog.tbrType = $scope.timeTypes[0];
    $scope.netlog.reportMS = 10;
    $scope.closeAlert(0);
  };
  $scope.userSchemaReset = function() {
    // clear client and server side form
    // $scope.pingData = {};
    // $scope.ping = angular.copy($scope.pingData);

    // clear client side form and reset defaults
    $scope.user_schema = angular.copy({});
    $scope.closeAlert(0);
  };
  // compare form data with in memory data
  $scope.pingReset();
  $scope.pingUnchanged = function(ping) {
    return angular.equals(ping, $scope.pingData);
  };
  /*$scope.owpReset();
  $scope.owpUnchanged = function(owp) {
    return angular.equals(owp, $scope.owpData);
  };*/
  $scope.perfReset();
  $scope.perfUnchanged = function(perf) {
    return angular.equals(perf, $scope.perfData);
  };
  $scope.netlogReset();
  $scope.netlogUnchanged = function(netlog) {
    return angular.equals(netlog, $scope.netlogData);
  };
  // $scope.userSchemaReset();
  $scope.userSchemaUnchanged = function(user_schema) {
    return angular.equals(user_schema, $scope.userSchemaData);
  };

  $scope.pingSubmit = function(ping) {
    if (ping.$invalid) {
      // If form is invalid, return and let AngularJS show validation errors.
      $scope.addAlert('Invalid form, cannot be submitted', 'danger');
      $scope.alert = true;
      return;
    } else {
      // Tell user form has been sent
      // $scope.addAlert('Data sent to UNIS. Please wait for confirmation.', 'info');
      // $scope.alert = true;

      // copy data submitted by form
      $scope.pingData = angular.copy(ping);

      // create proper interval for every based on user input
      var every;
      if($scope.pingData.tbtType.type === 'Days') {
        every = $scope.pingData.tbtValue * 86400;
      } else if($scope.pingData.tbtType.type === 'Hours') {
        every = $scope.pingData.tbtValue * 3600;
      } else if($scope.pingData.tbtType.type === 'Minutes') {
        every = $scope.pingData.tbtValue * 60;
      } else {
        every = $scope.pingData.tbtValue;
      }

      // lookup service running on given node
      var nodeService = $scope.getNodeService($scope.pingData.from.split(" ")[1]);

      // lookup port running on given node
      var nodePort = $scope.getNodePort($scope.pingData.to.split(" ")[1]);
      var portIP = $scope.getPortIP(nodePort);

      // build ping command from user options
      var ping_command = "ping -c 1 -s " + $scope.pingData.packetSize + " -i " + $scope.pingData.tbp + " " + portIP;

      // build ping measurement to submit
      var ping_measurement = {
        $schema: "http://unis.incntre.iu.edu/schema/20140214/measurement#",
        service: nodeService,
        ts: Math.round(new Date().getTime() * 1000),
        properties: {
          geni: {
            slice_uuid: $scope.geniSlice.slice_uuid
          }
        },
        eventTypes: [
          "ps:tools:blipp:linux:net:ping:ttl",
          "ps:tools:blipp:linux:net:ping:rtt"
        ],
        configuration: {
          status: "ON",
          regex: "ttl=(?P<ttl>\\d+).*time=(?P<rtt>\\d+\\.\\d+|\\d+)",
          reporting_params: parseInt($scope.pingData.reportMS),
          probe_module: "cmd_line_probe",
          packet_interval: parseInt($scope.pingData.tbp),
          collection_schedule: "builtins.simple",
          packet_size: parseInt($scope.pingData.packetSize),
          packet_count: 1,
          command: ping_command,
          schedule_params: {
            every: every,
            num_tests: parseInt($scope.pingData.num_tests)
          },
          collection_size: 100000,
          ms_url: $scope.geniSlice.ms_url,
          eventTypes: {
            rtt: "ps:tools:blipp:linux:net:ping:rtt",
            ttl: "ps:tools:blipp:linux:net:ping:ttl"
          },
          collection_ttl: 1500000,
          address: portIP,
          name: $scope.pingData.desc
        },
        type: "ping"
      };

      $http({
        method: 'POST',
        url: '/api/measurements',
        data: ping_measurement,
        headers: {'Content-type': 'application/perfsonar+json'}
      }).
      success(function(data, status, headers, config) {
        // $scope.addAlert(data, 'success');
        // $scope.addAlert(status, 'success');
        // $scope.addAlert(headers, 'success');
        // $scope.addAlert(config, 'success');
        $scope.addAlert('BLiPP Test: ' + data.configuration.name + ' submitted to UNIS', 'success');
        $scope.addAlert('Command: ' + ping_command, 'success');
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
  };
  /*$scope.owpSubmit = function(owp) {
    if (owp.$invalid) {
      // If form is invalid, return and let AngularJS show validation errors.
      $scope.addAlert('Invalid form, cannot be submitted', 'danger');
      $scope.alert = true;
      return;
    } else {
      // Tell user form has been sent
      // $scope.addAlert('Data sent to UNIS. Please wait for confirmation.', 'info');
      // $scope.alert = true;

      // copy data submitted by form
      $scope.owpData = angular.copy(owp);

      var owp_measurement = {
        "$schema": "http://unis.incntre.iu.edu/schema/20140214/measurement#",
        "service": "http://dev.incntre.iu.edu:8888/services/538fc810e7798940fc000091",
        "ts": Math.round(new Date().getTime() / 1000),
        "eventTypes": [
          // "ps:tools:blipp:linux:net:ping:owt",
          // "ps:tools:blipp:linux:net:ping:ttl"
        ],
        "configuration": {
          // "regex": "ttl=(?P<ttl>\\d+).*time=(?P<rtt>\\d+\\s|\\d+\\.\\d+)",
          // "reporting_params": $scope.pingData.reportMS,
          // "probe_module": "cmd_line_probe",
          "schedule_params": {
            // "every": $scope.pingData.tbtValue
          },
          "collection_schedule": "builtins.simple",
          // "command": "ping -c " + $scope.pingData.to,
          // "collection_size": $scope.pingData.packetSize,
          "ms_url": "http://localhost:8888",
          // "data_file": "/tmp/ops_ping.log",
          "eventTypes": {
            // "rtt": "ps:tools:blipp:linux:net:ping:rtt",
            // "ttl": "ps:tools:blipp:linux:net:ping:ttl"
          },
          // "collection_ttl": 1500000,
          "name": $scope.owpData.desc
        }
      };

      $http({
        method: 'POST',
        url: '/api/measurements',
        data: owp_measurement,
        headers: {'Content-type': 'application/perfsonar+json'}
      }).
      success(function(data, status, headers, config) {
        // $scope.addAlert(data, 'success');
        // $scope.addAlert(status, 'success');
        // $scope.addAlert(headers, 'success');
        // $scope.addAlert(config, 'success');
        var measurement = data;
        $scope.addAlert('BLiPP Test: ' + measurement.configuration.name + ' submitted to UNIS', 'success');
        $scope.alert = true;
      }).
      error(function(data, status, headers, config) {
        // $scope.addAlert(data, 'danger');
        // $scope.addAlert(status, 'danger');
        // $scope.addAlert(headers, 'danger');
        // $scope.addAlert(config, 'danger');
        var measurement = data;
        $scope.addAlert('Status: ' + status.toString() + ', ' + 'Error: ' + measurement.error.message, 'danger');
        $scope.alert = true;
      });
    }
  };*/

  $scope.perfSubmit = function(perf) {
    if (perf.$invalid) {
      // If form is invalid, return and let AngularJS show validation errors.
      $scope.addAlert('Invalid form, cannot be submitted', 'danger');
      $scope.alert = true;
      return;
    } else {
      // Tell user form has been sent
      // $scope.addAlert('Data sent to UNIS. Please wait for confirmation.', 'info');
      // $scope.alert = true;

      // copy data submitted by form
      $scope.perfData = angular.copy(perf);

      // create proper interval for every based on user input
      var every;
      if($scope.perfData.tbtType.type === 'Days') {
        every = $scope.perfData.tbtValue * 86400;
      } else if($scope.perfData.tbtType.type === 'Hours') {
        every = $scope.perfData.tbtValue * 3600;
      } else if($scope.perfData.tbtType.type === 'Minutes') {
        every = $scope.perfData.tbtValue * 60;
      } else {
        every = $scope.perfData.tbtValue;
      }

      // lookup port running on given node
      var nodePort = $scope.getNodePort($scope.perfData.to.split(" ")[1]);
      var portIP = $scope.getPortIP(nodePort);

      // build ping command from user options
      if ($scope.perfData.proto.type == 'udp') {
        var perf_command = "iperf -u -c " + portIP + " -t 20 -y C ";
      } else {
        var perf_command = "iperf -c " + portIP + " -t 20 -y C ";
      }

      // lookup service running on given node
      var nodeService = $scope.getNodeService($scope.perfData.to.split(" ")[1]);

      // build perf measurement to submit
      var perf_measurement = {
        $schema: "http://unis.incntre.iu.edu/schema/20140214/measurement#",
        service: nodeService,
        ts: Math.round(new Date().getTime() * 1000),
        properties: {
          geni: {
            slice_uuid: $scope.geniSlice.slice_uuid
          }
        },
        eventTypes: [
          "ps:tools:blipp:linux:net:iperf:bandwidth"
        ],
        configuration: {
          status: "ON",
          regex: ",(?P<bandwidth>\\d+)$",
          window_size: 0,
          protocol: $scope.perfData.proto.type,
          probe_module: "cmd_line_probe",
          test_duration: parseInt($scope.perfData.td),
          schedule_params: {
            every: every,
            num_tests: parseInt($scope.perfData.num_tests)
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
          name: $scope.perfData.desc
        },
        type: "iperf"
      };

      $http({
        method: 'POST',
        url: '/api/measurements',
        data: perf_measurement,
        headers: {'Content-type': 'application/perfsonar+json'}
      }).
      success(function(data, status, headers, config) {
        // $scope.addAlert(data, 'success');
        // $scope.addAlert(status, 'success');
        // $scope.addAlert(headers, 'success');
        // $scope.addAlert(config, 'success');
        $scope.addAlert('BLiPP Test: ' + data.configuration.name + ' submitted to UNIS', 'success');
        $scope.addAlert('Command: ' + perf_command, 'success');
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
  };
  $scope.netlogSubmit = function(netlog) {
    if (netlog.$invalid) {
      // If form is invalid, return and let AngularJS show validation errors.
      $scope.addAlert('Invalid form, cannot be submitted', 'danger');
      $scope.alert = true;
      return;
    } else {
      // Tell user form has been sent
      // $scope.addAlert('Data sent to UNIS. Please wait for confirmation.', 'info');
      // $scope.alert = true;

      // copy data submitted by form
      $scope.netlogData = angular.copy(netlog);

      // create proper interval for every based on user input
      var every;
      if($scope.netlogData.tbrType.type === 'Days') {
        every = $scope.netlogData.tbrValue * 86400;
      } else if($scope.netlogData.tbrType.type === 'Hours') {
        every = $scope.netlogData.tbrValue * 3600;
      } else if($scope.netlogData.tbrType.type === 'Minutes') {
        every = $scope.netlogData.tbrValue * 60;
      } else {
        every = $scope.netlogData.tbrValue;
      }

      // lookup service running on given node
      var nodeService = $scope.getNodeService($scope.netlogData.from.split(" ")[1]);

      // build netlogger measurement to submit
      var netlog_measurement = {
        $schema: "http://unis.incntre.iu.edu/schema/20140214/measurement#",
        service: nodeService,
        ts: Math.round(new Date().getTime() * 1000),
        properties: {
          geni: {
            slice_uuid: $scope.geniSlice.slice_uuid
          }
        },
        eventTypes: [ ],
        configuration: {
          status: "ON",
          reporting_params: parseInt($scope.netlogData.reportMS),
          name: $scope.netlogData.desc,
          schedule_params: {
            every: every,
            num_tests: parseInt($scope.netlogData.num_tests)
          },
          collection_schedule: "builtins.simple",
          ms_url: $scope.geniSlice.ms_url,
          logfile: $scope.netlogData.file,
          probe_module: "netlogger_probe"
        },
        type: "netlogger"
      };

      $http({
        method: 'POST',
        url: '/api/measurements',
        data: netlog_measurement,
        headers: {'Content-type': 'application/perfsonar+json'}
      }).
      success(function(data, status, headers, config) {
        // $scope.addAlert(data, 'success');
        // $scope.addAlert(status, 'success');
        // $scope.addAlert(headers, 'success');
        // $scope.addAlert(config, 'success');
        $scope.addAlert('BLiPP Test: ' + data.configuration.name + ' submitted to UNIS', 'success');
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
  };
}); // end controller
