/*
 * API and Browser Routes
 * app/
 * routes.js
 */

// var Node = require('./models/node')
// , Service = require('./models/service');
var fs = require('fs')
  , path = require('path')
  , http = require('http')
  , https = require('https')
  , url = require('url');

// UNIS production config
// var production = true;
// var unis_host = 'unis.incntre.iu.edu';
// var unis_port = '8443';
var unis_cert = '/usr/local/etc/certs/unis-proxy.pem';
var unis_key = '/usr/local/etc/certs/unis-proxy.pem';

// UNIS development config
var production = false;
var unis_host = 'dev.incntre.iu.edu';
// var unis_host = 'localhost';
var unis_port = '8888';
var idms_host = 'monitor.incntre.iu.edu'
var idms_port = '9000';

// Measurement Store config
var ms_host = 'dev.incntre.iu.edu';
// var ms_host = 'localhost';
var ms_port = '8888';
var idms_ms_host = 'monitor.incntre.iu.edu';
var idms_ms_port = '9001';

var slice_info = [];
var filePath = '/usr/local/etc/node.info';
var slice_uuid = '';
var os_name = '';
var distro = '';

module.exports = function(app) {
   var self = this ;  
  console.log("UNIS Instance: " + unis_host + "@" + unis_port);

  var exec = require('child_process').exec;
  var child1, child2;

  child1 = exec('uname -s',
    function (error, stdout, stderr) {
      os_name = stdout;
      if (error !== null) {
        console.log('exec error: ' + error);
      }
  });

  child2 = exec('head -1 /etc/issue',
    function (error, stdout, stderr) {
      distro = stdout;
      if (error !== null) {
        console.log('exec error: ' + error);
      }
  });

  fs.readFile(filePath, {encoding: 'utf-8'}, function(err, data) {
    if (err) {
      console.log('file read error: ' + err);
    } else {
      var fileData = data.toString().split('\n');
      var split, project, slice, gn, exAddy, ms_url, unis;

      for(line in fileData) {
        split = fileData[line].split('=');

        if(split[0] === 'external_address')
          exAddy = split[1];

        if (split[0] === 'gn_address')
          gn = split[1];

        if(split[0] === 'unis_instance')
          unis = split[1];

        if(split[0] === 'ms_instance') {
          ms_url = split[1];
          // ms_port = ms_url.split(":")[2];
          console.log("Measurement Store Port: " + ms_port);
          // ms_host = ms_url.split("//")[1].split(":")[0];
          console.log("Measurement Store Host: " + ms_host);
        }

        if (split[0] === 'node_id') {
          project = split[2].split('+');
          slice = project[3].split(':');
        }

        if(split[0] === 'auth_uuid')
          slice_uuid = split[1];
      }
      slice_info.push({'external_address': exAddy, 'gn_address': gn, 'unis_instance': unis, 'ms_url': ms_url, 'project': project[1], 'slice': slice[0], 'slice_uuid': slice_uuid, 'os_name': os_name, 'distro': distro});
      // console.log(slice_info);
    }
  });

  app.get('/unis', function(req, res) {
    // console.log('STATUS: ' + res.statusCode);
    // console.log('HEADERS: ' + JSON.stringify(res.headers));
    // console.log('BODY: ' + JSON.stringify(res.body));

    var routes = [];
    var hostname = req.headers.host;
    var pathname = url.parse(req.url).pathname;

    routes.push('http://' + hostname + pathname + '/slice');
    routes.push('http://' + hostname + pathname + '/nodes');
    routes.push('http://' + hostname + pathname + '/services');
    routes.push('http://' + hostname + pathname + '/measurements');
    routes.push('http://' + hostname + pathname + '/metadata');
    routes.push('http://' + hostname + pathname + '/data');
    routes.push('http://' + hostname + pathname + '/links');
    routes.push('http://' + hostname + pathname + '/ports');
    routes.push('http://' + hostname + pathname + '/domains');
    routes.push('http://' + hostname + '/unis/idms');

    res.json(routes);
  });

  app.get('/unis/idms', function(req, res) {
    // console.log('STATUS: ' + res.statusCode);
    // console.log('HEADERS: ' + JSON.stringify(res.headers));
    // console.log('BODY: ' + JSON.stringify(res.body));

    var routes = [];
    var hostname = req.headers.host;
    var pathname = url.parse(req.url).pathname;

    routes.push('http://' + hostname + pathname + '/nodes');
    routes.push('http://' + hostname + pathname + '/services');
    routes.push('http://' + hostname + pathname + '/measurements');
    routes.push('http://' + hostname + pathname + '/metadata');
    routes.push('http://' + hostname + pathname + '/data');
    routes.push('http://' + hostname + '/unis');

    res.json(routes);
  });

  app.get('/unis/slice', function(req, res) {
    // console.log('STATUS: ' + res.statusCode);
    // console.log('HEADERS: ' + JSON.stringify(res.headers));
    // console.log('BODY: ' + JSON.stringify(res.body));

    console.log(slice_info);
    res.json(slice_info);
  });

  app.get('/unis/nodes', function(req, res) {
    // console.log('STATUS: ' + res.statusCode);
    // console.log('HEADERS: ' + JSON.stringify(res.headers));
    // console.log('BODY: ' + JSON.stringify(res.body));

    if (production) {
      console.log('running in production');

      /* HTTPS Options */
      var https_get_options = {
        hostname: unis_host,
        port: unis_port,
        key: fs.readFileSync(unis_key),
        cert: fs.readFileSync(unis_cert),
        requestCert: true,
        rejectUnauthorized: false,
        path: '/nodes?properties.geni.slice_uuid=' + slice_uuid,
        // path: '/nodes',
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      /* GET JSON and Render to our API */
      https.get(https_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    } else {
      /* HTTP Options */
      var http_get_options = {
        hostname: unis_host,
        port: unis_port,
        path: '/nodes?limit=10',
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      /* GET JSON and Render to our API */
      http.get(http_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    }
    /* Access Model Created from Mongo */
    /*Node.find(function(err, nodes) {

      if (err)
        res.send(err);

      console.log(nodes);
      res.json(nodes);
    });*/
  });

  app.get('/unis/nodes/:id', function(req, res) {
    console.log("node id: " + req.params.id);
    // console.log('STATUS: ' + res.statusCode);
    // console.log('HEADERS: ' + JSON.stringify(res.headers));
    // console.log('BODY: ' + JSON.stringify(res.body));

    var node_id = req.params.id;

    if (production) {
      console.log('running in production');

      /* HTTPS Options */
      var https_get_options = {
        hostname: unis_host,
        port: unis_port,
        key: fs.readFileSync(unis_key),
        cert: fs.readFileSync(unis_cert),
        requestCert: true,
        rejectUnauthorized: false,
        path: '/nodes/' + node_id + '?properties.geni.slice_uuid=' + slice_uuid,
        // path: '/nodes/' + node_id,
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      /* GET JSON and Render to our API */
      https.get(https_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    } else {
      /* HTTP Options */
      var http_get_options = {
        hostname: unis_host,
        port: unis_port,
        path: '/nodes/' + node_id,
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      /* GET JSON and Render to our API */
      http.get(http_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    }
  });

  app.get('/unis/services', function(req, res) {
    // console.log('STATUS: ' + res.statusCode);
    // console.log('HEADERS: ' + JSON.stringify(res.headers));
    // console.log('BODY: ' + JSON.stringify(res.body));

    if (production) {
      console.log('running in production');

      /* HTTPS Options */
      var https_get_options = {
        hostname: unis_host,
        port: unis_port,
        key: fs.readFileSync(unis_key),
        cert: fs.readFileSync(unis_cert),
        requestCert: true,
        rejectUnauthorized: false,
        path: '/services?properties.geni.slice_uuid=' + slice_uuid,
        // path: '/services',
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      /* GET JSON and Render to our API */
      https.get(https_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    } else {
      /* HTTP Options */
      var http_get_options = {
        hostname: unis_host,
        port: unis_port,
        path: '/services',
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      /* GET JSON and Render to our API */
      http.get(http_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    }
    /* Access Model Created from Mongo */
    /*Service.find(function(err, services) {

      if (err)
        res.send(err);

      console.log(services);
      res.json(services);
    });*/
  });

  app.get('/unis/services/:id', function(req, res) {
    console.log("service id: " + req.params.id);
    // console.log('STATUS: ' + res.statusCode);
    // console.log('HEADERS: ' + JSON.stringify(res.headers));
    // console.log('BODY: ' + JSON.stringify(res.body));

    var service_id = req.params.id;

    if (production) {
      console.log('running in production');

      /* HTTPS Options */
      var https_get_options = {
        hostname: unis_host,
        port: unis_port,
        key: fs.readFileSync(unis_key),
        cert: fs.readFileSync(unis_cert),
        requestCert: true,
        rejectUnauthorized: false,
        path: '/services/' + service_id + '?properties.geni.slice_uuid=' + slice_uuid,
        // path: '/services/' + service_id,
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      /* GET JSON and Render to our API */
      https.get(https_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    } else {
      /* HTTP Options */
      var http_get_options = {
          hostname: unis_host,
          port: unis_port,
          path: '/services/' + service_id,
          method: 'GET',
          headers: {
              'Content-type': 'application/perfsonar+json',
              'connection': 'keep-alive'
          }
      };
      /* GET JSON and Render to our API */
      http.get(http_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    }
  });

  app.get('/unis/measurements', function(req, res) {
    // console.log('STATUS: ' + res.statusCode);
    // console.log('HEADERS: ' + JSON.stringify(res.headers));
    // console.log('BODY: ' + JSON.stringify(res.body));

    if (production) {
      console.log('running in production');

      /* HTTPS Options */
      var https_get_options = {
        hostname: unis_host,
        port: unis_port,
        key: fs.readFileSync(unis_key),
        cert: fs.readFileSync(unis_cert),
        requestCert: true,
        rejectUnauthorized: false,
        path: '/measurements?properties.geni.slice_uuid=' + slice_uuid,
        // path: '/measurements',
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      /* GET JSON and Render to our API */
      https.get(https_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    } else {
      /* HTTP Options */
      var http_get_options = {
          hostname: unis_host,
          port: unis_port,
          path: '/measurements',
          method: 'GET',
          headers: {
              'Content-type': 'application/perfsonar+json',
              'connection': 'keep-alive'
          }
      };
      /* GET JSON and Render to our API */
      http.get(http_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    }
  });

  app.get('/unis/measurements/:id', function(req, res) {
    console.log("measurement id: " + req.params.id);
    // console.log('STATUS: ' + res.statusCode);
    // console.log('HEADERS: ' + JSON.stringify(res.headers));
    // console.log('BODY: ' + JSON.stringify(res.body));

    var measurement_id = req.params.id;

    if (production) {
      console.log('running in production');

      /* HTTPS Options */
      var https_get_options = {
        hostname: unis_host,
        port: unis_port,
        key: fs.readFileSync(unis_key),
        cert: fs.readFileSync(unis_cert),
        requestCert: true,
        rejectUnauthorized: false,
        path: '/measurements/' + measurement_id + '?properties.geni.slice_uuid=' + slice_uuid,
        // path: '/measurements/' + measurement_id,
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      /* GET JSON and Render to our API */
      https.get(https_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    } else {
      /* HTTP Options */
      var http_get_options = {
        hostname: unis_host,
        port: unis_port,
        path: '/measurements/' + measurement_id,
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      /* GET JSON and Render to our API */
      http.get(http_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    }
  });

  app.post('/unis/measurements', function(req, res) {
    console.log('STATUS: ' + res.statusCode);
    console.log("post length: " + req.body.length);
    console.log('HEADERS: ' + JSON.stringify(res.headers));
    console.log('BODY: ' + JSON.stringify(res.body));

    // store result
    var post_data = JSON.stringify(req.body);

    if (production) {
      console.log('running in production');

      /* HTTPS Options */
      var https_post_options = {
        hostname: unis_host,
        port: unis_port,
        key: fs.readFileSync(unis_key),
        cert: fs.readFileSync(unis_cert),
        requestCert: true,
        rejectUnauthorized: false,
        path: '/measurements?properties.geni.slice_uuid=' + slice_uuid,
        // path: '/measurements',
        method: 'POST',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'Content-Length': post_data.length
        }
      };
      // POST form measurement data to UNIS
      var post_req = https.request(https_post_options, function(http_res) {
        // used to gather chunks
        var data = '';

        console.log('STATUS: ' + http_res.statusCode);
        console.log('HEADERS: ' + JSON.stringify(http_res.headers));
        http_res.setEncoding('utf8');
        http_res.on('data', function (chunk) {
          console.log('BODY: ' + chunk);
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log("return obj: " + JSON.stringify(obj));
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });

      post_req.on('error', function(e) {
        console.log('problem with request: ' + e.message);
        res.send(404);
      });

      console.log("post_data: " + post_data);

      // write data to request body
      post_req.write(post_data);
      post_req.end();
    } else {
      // HTTP Options
      var http_post_options = {
          hostname: unis_host,
          port: unis_port,
          path: '/measurements',
          method: 'POST',
          headers: {
              'Content-type': 'application/perfsonar+json',
              'Content-Length': post_data.length
          }
      };
      // POST form measurement data to UNIS
      var post_req = http.request(http_post_options, function(http_res) {
        // used to gather chunks
        var data = '';

        console.log('STATUS: ' + http_res.statusCode);
        console.log('HEADERS: ' + JSON.stringify(http_res.headers));
        http_res.setEncoding('utf8');
        http_res.on('data', function (chunk) {
          console.log('BODY: ' + chunk);
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log("return obj: " + JSON.stringify(obj));
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });

      post_req.on('error', function(e) {
        console.log('problem with request: ' + e.message);
        res.send(404);
      });

      console.log("post_data: " + post_data);

      // write data to request body
      post_req.write(post_data);
      post_req.end();
    }
  });

  app.put('/unis/measurements/:id', function(req, res) {
    console.log("measurement id: " + req.params.id);
    console.log("put length: " + req.body.length);
    console.log('STATUS: ' + res.statusCode);
    console.log('HEADERS: ' + JSON.stringify(res.headers));
    console.log('BODY: ' + JSON.stringify(res.body));

    // store results
    var measurement_id = req.params.id;
    var put_data = JSON.stringify(req.body);
    console.log("put length: " + put_data.length);

    if (production) {
      console.log('running in production');

      /* HTTPS Options */
      var https_put_options = {
        hostname: unis_host,
        port: unis_port,
        key: fs.readFileSync(unis_key),
        cert: fs.readFileSync(unis_cert),
        requestCert: true,
        rejectUnauthorized: false,
        path: '/measurements/' + measurement_id + '?properties.geni.slice_uuid=' + slice_uuid,
        // path: '/measurements/' + measurement_id,
        method: 'PUT',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'Content-Length': put_data.length
        }
      };
      // POST form measurement data to UNIS
      var put_req = https.request(https_put_options, function(http_res) {
        // used to gather chunks
        var data = '';

        console.log('STATUS: ' + http_res.statusCode);
        console.log('HEADERS: ' + JSON.stringify(http_res.headers));

        http_res.setEncoding('utf8');

        http_res.on('data', function (chunk) {
          console.log('BODY: ' + chunk);
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log("return obj: " + JSON.stringify(obj));
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });

      put_req.on('error', function(e) {
        console.log('problem with request: ' + e.message);
        res.send(404);
      });

      console.log("put_data: " + put_data);

      // write data to request body
      put_req.write(put_data);
      put_req.end();
    } else {
      // HTTP Options
      var http_put_options = {
          hostname: unis_host,
          port: unis_port,
          path: '/measurements/' + measurement_id,
          method: 'PUT',
          headers: {
              'Content-type': 'application/perfsonar+json',
              'Content-Length': put_data.length
          }
      };
      // POST form measurement data to UNIS
      var put_req = http.request(http_put_options, function(http_res) {
        // used to gather chunks
        var data = '';

        console.log('STATUS: ' + http_res.statusCode);
        console.log('HEADERS: ' + JSON.stringify(http_res.headers));

        http_res.setEncoding('utf8');

        http_res.on('data', function (chunk) {
          console.log('BODY: ' + chunk);
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log("return obj: " + JSON.stringify(obj));
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });

      put_req.on('error', function(e) {
        console.log('problem with request: ' + e.message);
        res.send(404);
      });

      console.log("put_data: " + put_data);

      // write data to request body
      put_req.write(put_data);
      put_req.end();
    }
  });

  app.delete('/unis/measurements/:id', function(req, res) {
    console.log("measurement id: " + req.params.id);
    console.log("delete length: " + req.body.length);
    console.log('STATUS: ' + res.statusCode);
    console.log('HEADERS: ' + JSON.stringify(res.headers));
    console.log('BODY: ' + JSON.stringify(res.body));

    // store result
    var measurement_id = req.params.id;
    var delete_data = JSON.stringify(req.body);

    if (production) {
      console.log('running in production');

      /* HTTPS Options */
      var https_delete_options = {
        hostname: unis_host,
        port: unis_port,
        key: fs.readFileSync(unis_key),
        cert: fs.readFileSync(unis_cert),
        requestCert: true,
        rejectUnauthorized: false,
        path: '/measurements/' + measurement_id + '?properties.geni.slice_uuid=' + slice_uuid,
        // path: '/measurements/' + measurement_id,
        method: 'DELETE',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'Content-Length': delete_data.length
        }
      };
      // DELETE measurement from UNIS
      var delete_req = http.request(https_delete_options, function(http_res) {
        // used to gather chunks
        var data = '';

        console.log('STATUS: ' + http_res.statusCode);
        console.log('HEADERS: ' + JSON.stringify(http_res.headers));
        console.log('BODY: ' + JSON.stringify(res.body));

        http_res.setEncoding('utf8');

        http_res.on('data', function (chunk) {
          console.log('BODY: ' + chunk);
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log("return obj: " + JSON.stringify(obj));
          res.send( 200 );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });

      delete_req.on('error', function(e) {
        console.log('problem with request: ' + e.message);
        res.send( 404 );
      });

      console.log("delete_data: " + delete_data);
      delete_req.write(delete_data);
      delete_req.end();
    } else {
      /* HTTP Options */
      var http_delete_options = {
          hostname: unis_host,
          port: unis_port,
          path: '/measurements/' + measurement_id,
          method: 'DELETE',
          headers: {
              'Content-type': 'application/perfsonar+json',
              'Content-Length': delete_data.length
          }
      };
      // DELETE measurement from UNIS
      var delete_req = http.request(http_delete_options, function(http_res) {
        // used to gather chunks
        var data = '';

        console.log('STATUS: ' + http_res.statusCode);
        console.log('HEADERS: ' + JSON.stringify(http_res.headers));
        console.log('BODY: ' + JSON.stringify(res.body));

        http_res.setEncoding('utf8');

        http_res.on('data', function (chunk) {
          console.log('BODY: ' + chunk);
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log("return obj: " + JSON.stringify(obj));
          res.send( 200 );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });

      delete_req.on('error', function(e) {
        console.log('problem with request: ' + e.message);
        res.send( 404 );
      });

      console.log("delete_data: " + delete_data);
      delete_req.write(delete_data);
      delete_req.end();
    }
  });

  app.get('/unis/metadata', function(req, res) {
    // console.log('STATUS: ' + res.statusCode);
    // console.log('HEADERS: ' + JSON.stringify(res.headers));
    // console.log('BODY: ' + JSON.stringify(res.body));

    if (production) {
      console.log('running in production');

      /* HTTPS Options */
      var https_get_options = {
        hostname: unis_host,
        port: unis_port,
        key: fs.readFileSync(unis_key),
        cert: fs.readFileSync(unis_cert),
        requestCert: true,
        rejectUnauthorized: false,
        path: '/metadata?parameters.geni.slice_uuid=' + slice_uuid,
        // path: '/metadata',
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      /* GET JSON and Render to our API */
      https.get(https_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    } else {
      /* HTTP Options */
      var http_get_options = {
          hostname: unis_host,
          port: unis_port,
          path: '/metadata',
          method: 'GET',
          headers: {
              'Content-type': 'application/perfsonar+json',
              'connection': 'keep-alive'
          }
      };
      /* GET JSON and Render to our API */
      http.get(http_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    }
  });

  app.get('/unis/metadata/:id', function(req, res) {
    console.log("metadata id: " + req.params.id);
    // console.log('STATUS: ' + res.statusCode);
    // console.log('HEADERS: ' + JSON.stringify(res.headers));
    // console.log('BODY: ' + JSON.stringify(res.body));

    var metadata_id = req.params.id;

    if (production) {
      console.log('running in production');

      /* HTTPS Options */
      var https_get_options = {
        hostname: unis_host,
        port: unis_port,
        key: fs.readFileSync(unis_key),
        cert: fs.readFileSync(unis_cert),
        requestCert: true,
        rejectUnauthorized: false,
        path: '/metadata/' + metadata_id + '?parameters.geni.slice_uuid=' + slice_uuid,
        // path: '/metadata/' + metadata_id,
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      /* GET JSON and Render to our API */
      https.get(https_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    } else {
      /* HTTP Options */
      var http_get_options = {
        hostname: unis_host,
        port: unis_port,
        path: '/metadata/' + metadata_id,
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      /* GET JSON and Render to our API */
      http.get(http_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    }
  });

  app.get('/unis/data', function(req, res) {
    // console.log('STATUS: ' + res.statusCode);
    // console.log('HEADERS: ' + JSON.stringify(res.headers));
    // console.log('BODY: ' + JSON.stringify(res.body));

    if (production) {
      console.log('running in production');

      // HTTPS Options
      var https_get_options = {
        hostname: ms_host,
        port: ms_port,
        key: fs.readFileSync(unis_key),
        cert: fs.readFileSync(unis_cert),
        requestCert: true,
        rejectUnauthorized: false,
        // path: '/data?properties.geni.slice_uuid=' + slice_uuid,
        path: '/data',
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      // GET JSON and Render to our API
      https.get(https_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    } else {
      // HTTP Options
      var http_get_options = {
          hostname: ms_host,
          port: ms_port,
          path: '/data',
          method: 'GET',
          headers: {
              'Content-type': 'application/perfsonar+json',
              'connection': 'keep-alive'
          }
      };
      // GET JSON and Render to our API
      http.get(http_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    }
  });

  app.get('/unis/data/:id', function(req, res) {
    console.log("data id: " + req.params.id);
    // console.log('STATUS: ' + res.statusCode);
    // console.log('HEADERS: ' + JSON.stringify(res.headers));
    // console.log('BODY: ' + JSON.stringify(res.body));

    var data_id = req.params.id;

    if (production) {
      console.log('running in production');

      // HTTPS Options
      var https_get_options = {
        hostname: ms_host,
        port: ms_port,
        key: fs.readFileSync(unis_key),
        cert: fs.readFileSync(unis_cert),
        requestCert: true,
        rejectUnauthorized: false,
        // path: '/data/' + data_id + '?properties.geni.slice_uuid=' + slice_uuid,
        path: '/data/' + data_id,
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      // GET JSON and Render to our API
      https.get(https_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    } else {
      // HTTP Options
      var http_get_options = {
        hostname: ms_host,
        port: ms_port,
        path: '/data/' + data_id,
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      // GET JSON and Render to our API
      http.get(http_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    }
  });

  app.get('/unis/links', function(req, res) {
    // console.log('STATUS: ' + res.statusCode);
    // console.log('HEADERS: ' + JSON.stringify(res.headers));
    // console.log('BODY: ' + JSON.stringify(res.body));

    if (production) {
      console.log('running in production');

      /* HTTPS Options */
      var https_get_options = {
        hostname: unis_host,
        port: unis_port,
        key: fs.readFileSync(unis_key),
        cert: fs.readFileSync(unis_cert),
        requestCert: true,
        rejectUnauthorized: false,
        path: '/links?properties.geni.slice_uuid=' + slice_uuid,
        // path: '/links',
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      /* GET JSON and Render to our API */
      https.get(https_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    } else {
      /* HTTP Options */
      var http_get_options = {
          hostname: unis_host,
          port: unis_port,
          path: '/links',
          method: 'GET',
          headers: {
              'Content-type': 'application/perfsonar+json',
              'connection': 'keep-alive'
          }
      };
      /* GET JSON and Render to our API */
      http.get(http_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    }
  });

  app.get('/unis/links/:id', function(req, res) {
    console.log("link id: " + req.params.id);
    // console.log('STATUS: ' + res.statusCode);
    // console.log('HEADERS: ' + JSON.stringify(res.headers));
    // console.log('BODY: ' + JSON.stringify(res.body));

    var link_id = req.params.id;

    if (production) {
      console.log('running in production');

      /* HTTPS Options */
      var https_get_options = {
        hostname: unis_host,
        port: unis_port,
        key: fs.readFileSync(unis_key),
        cert: fs.readFileSync(unis_cert),
        requestCert: true,
        rejectUnauthorized: false,
        path: '/links/' + link_id + '?properties.geni.slice_uuid=' + slice_uuid,
        // path: '/links/' + link_id,
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      /* GET JSON and Render to our API */
      https.get(https_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    } else {
      /* HTTP Options */
      var http_get_options = {
        hostname: unis_host,
        port: unis_port,
        path: '/links/' + link_id,
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      /* GET JSON and Render to our API */
      http.get(http_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    }
  });

  app.get('/unis/ports', function(req, res) {
    // console.log('STATUS: ' + res.statusCode);
    // console.log('HEADERS: ' + JSON.stringify(res.headers));
    // console.log('BODY: ' + JSON.stringify(res.body));

    if (production) {
      console.log('running in production');

      /* HTTPS Options */
      var https_get_options = {
        hostname: unis_host,
        port: unis_port,
        key: fs.readFileSync(unis_key),
        cert: fs.readFileSync(unis_cert),
        requestCert: true,
        rejectUnauthorized: false,
        path: '/ports?properties.geni.slice_uuid=' + slice_uuid,
        // path: '/ports',
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      /* GET JSON and Render to our API */
      https.get(https_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    } else {
      /* HTTP Options */
      var http_get_options = {
          hostname: unis_host,
          port: unis_port,
          path: '/ports',
          method: 'GET',
          headers: {
              'Content-type': 'application/perfsonar+json',
              'connection': 'keep-alive'
          }
      };
      /* GET JSON and Render to our API */
      http.get(http_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    }
  });

  app.get('/unis/ports/:id', function(req, res) {
    console.log("port id: " + req.params.id);
    // console.log('STATUS: ' + res.statusCode);
    // console.log('HEADERS: ' + JSON.stringify(res.headers));
    // console.log('BODY: ' + JSON.stringify(res.body));

    var port_id = req.params.id;

    if (production) {
      console.log('running in production');

      /* HTTPS Options */
      var https_get_options = {
        hostname: unis_host,
        port: unis_port,
        key: fs.readFileSync(unis_key),
        cert: fs.readFileSync(unis_cert),
        requestCert: true,
        rejectUnauthorized: false,
        path: '/ports/' + port_id + '?properties.geni.slice_uuid=' + slice_uuid,
        // path: '/ports/' + port_id,
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      /* GET JSON and Render to our API */
      https.get(https_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    } else {
      /* HTTP Options */
      var http_get_options = {
        hostname: unis_host,
        port: unis_port,
        path: '/ports/' + port_id,
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      /* GET JSON and Render to our API */
      http.get(http_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    }
  });

  app.get('/unis/domains', function(req, res) {
    // console.log('STATUS: ' + res.statusCode);
    // console.log('HEADERS: ' + JSON.stringify(res.headers));
    // console.log('BODY: ' + JSON.stringify(res.body));

    if (production) {
      console.log('running in production');

      /* HTTPS Options */
      var https_get_options = {
        hostname: unis_host,
        port: unis_port,
        key: fs.readFileSync(unis_key),
        cert: fs.readFileSync(unis_cert),
        requestCert: true,
        rejectUnauthorized: false,
        path: '/domains?properties.geni.slice_uuid=' + slice_uuid,
        // path: '/domains',
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      /* GET JSON and Render to our API */
      https.get(https_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    } else {
      /* HTTP Options */
      var http_get_options = {
          hostname: unis_host,
          port: unis_port,
          path: '/domains',
          method: 'GET',
          headers: {
              'Content-type': 'application/perfsonar+json',
              'connection': 'keep-alive'
          }
      };
      /* GET JSON and Render to our API */
      http.get(http_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    }
  });

  app.get('/unis/domains/:id', function(req, res) {
    console.log("domain id: " + req.params.id);
    // console.log('STATUS: ' + res.statusCode);
    // console.log('HEADERS: ' + JSON.stringify(res.headers));
    // console.log('BODY: ' + JSON.stringify(res.body));

    var domain_id = req.params.id;

    if (production) {
      console.log('running in production');

      /* HTTPS Options */
      var https_get_options = {
        hostname: unis_host,
        port: unis_port,
        key: fs.readFileSync(unis_key),
        cert: fs.readFileSync(unis_cert),
        requestCert: true,
        rejectUnauthorized: false,
        path: '/domains/' + domain_id + '?properties.geni.slice_uuid=' + slice_uuid,
        // path: '/domains/' + domain_id,
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      /* GET JSON and Render to our API */
      https.get(https_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    } else {
      /* HTTP Options */
      var http_get_options = {
        hostname: unis_host,
        port: unis_port,
        path: '/domains/' + domain_id,
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      /* GET JSON and Render to our API */
      http.get(http_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    }
  });

  app.get('/unis/idms/nodes', function(req, res) {
    // console.log('STATUS: ' + res.statusCode);
    // console.log('HEADERS: ' + JSON.stringify(res.headers));
    // console.log('BODY: ' + JSON.stringify(res.body));

    if (production) {
      console.log('running in production');

      /* HTTPS Options */
      var https_get_options = {
        hostname: idms_host,
        port: idms_port,
        key: fs.readFileSync(unis_key),
        cert: fs.readFileSync(unis_cert),
        requestCert: true,
        rejectUnauthorized: false,
        path: '/nodes?properties.geni.slice_uuid=' + slice_uuid,
        // path: '/nodes',
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      /* GET JSON and Render to our API */
      https.get(https_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    } else {
      /* HTTP Options */
      var http_get_options = {
        hostname: idms_host,
        port: idms_port,
        path: '/nodes',
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      /* GET JSON and Render to our API */
      http.get(http_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    }
  });

  app.get('/unis/idms/nodes/:id', function(req, res) {
    console.log("node id: " + req.params.id);
    // console.log('STATUS: ' + res.statusCode);
    // console.log('HEADERS: ' + JSON.stringify(res.headers));
    // console.log('BODY: ' + JSON.stringify(res.body));

    var node_id = req.params.id;

    if (production) {
      console.log('running in production');

      /* HTTPS Options */
      var https_get_options = {
        hostname: idms_host,
        port: idms_port,
        key: fs.readFileSync(unis_key),
        cert: fs.readFileSync(unis_cert),
        requestCert: true,
        rejectUnauthorized: false,
        path: '/nodes/' + node_id + '?properties.geni.slice_uuid=' + slice_uuid,
        // path: '/nodes/' + node_id,
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      /* GET JSON and Render to our API */
      https.get(https_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    } else {
      /* HTTP Options */
      var http_get_options = {
        hostname: idms_host,
        port: idms_port,
        path: '/nodes/' + node_id,
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      /* GET JSON and Render to our API */
      http.get(http_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    }
  });

  self.getIdmsServices = (function(cb){
	  
	  if (production) {
		  console.log('running in production');
		  
		  /* HTTPS Options */
		  var https_get_options = {
				  hostname: idms_host,
				  port: idms_port,
				  key: fs.readFileSync(unis_key),
				  cert: fs.readFileSync(unis_cert),
				  requestCert: true,
				  rejectUnauthorized: false,
				  path: '/services?properties.geni.slice_uuid=' + slice_uuid,
				  // path: '/services',
				  method: 'GET',
				  headers: {
					  'Content-type': 'application/perfsonar+json',
					  'connection': 'keep-alive'
				  }
		  };
		  /* GET JSON and Render to our API */
		  https.get(https_get_options, function(http_res) {
			  var data = '';
			  
			  http_res.on('data', function (chunk) {
				  data += chunk;
			  });
			  http_res.on('end',function() {
				  var obj = JSON.parse(data);
				  // console.log( obj );
				  cb({data:obj , type : 'json'});
			  });
			  http_res.on('error',function() {
				  console.log('problem with request: ' + e.message);
				  cb({data: {} , type : '404'});				  
			  });
		  });
	  } else {
		  /* HTTP Options */
		  var http_get_options = {
				  hostname: idms_host,
				  port: idms_port,
				  path: '/services',
				  method: 'GET',
				  headers: {
					  'Content-type': 'application/perfsonar+json',
					  'connection': 'keep-alive'
				  }
		  };
		  /* GET JSON and Render to our API */
		  http.get(http_get_options, function(http_res) {
			  var data = '';
			  
			  http_res.on('data', function (chunk) {
				  data += chunk;
			  });
			  http_res.on('end',function() {
				  var obj = JSON.parse(data);
				  // console.log( obj );
				  cb({data:obj , type : 'json'});
			  });
			  http_res.on('error',function() {
				  console.log('problem with request: ' + e.message);
				  cb({data: {} , type : '404'});		
			  });
		  });
	  }
  });
  app.get('/unis/idms/services', function(req, res) {
    // console.log('STATUS: ' + res.statusCode);
    // console.log('HEADERS: ' + JSON.stringify(res.headers));
    // console.log('BODY: ' + JSON.stringify(res.body));
    /* Access Model Created from Mongo */
	  var services = self.getIdmsServices(function(j){
		  var data = j.data , type = j.type ;
		  switch(type){
			  case 'json' : res.json(data);
			  break
			  case '404' : res.send(404);
			  break;
			  default :   res.send(404);
		  }
	  });
    /*Service.find(function(err, services) {
	
      if (err)
        res.send(err);
	
      console.log(services);
      res.json(services);
    });*/
  });

  app.get('/unis/idms/services/:id', function(req, res) {
    console.log("service id: " + req.params.id);
    // console.log('STATUS: ' + res.statusCode);
    // console.log('HEADERS: ' + JSON.stringify(res.headers));
    // console.log('BODY: ' + JSON.stringify(res.body));

    var service_id = req.params.id;

    if (production) {
      console.log('running in production');

      /* HTTPS Options */
      var https_get_options = {
        hostname: idms_host,
        port: idms_port,
        key: fs.readFileSync(unis_key),
        cert: fs.readFileSync(unis_cert),
        requestCert: true,
        rejectUnauthorized: false,
        path: '/services/' + service_id + '?properties.geni.slice_uuid=' + slice_uuid,
        // path: '/services/' + service_id,
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      /* GET JSON and Render to our API */
      https.get(https_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    } else {
      /* HTTP Options */
      var http_get_options = {
          hostname: idms_host,
          port: idms_port,
          path: '/services/' + service_id,
          method: 'GET',
          headers: {
              'Content-type': 'application/perfsonar+json',
              'connection': 'keep-alive'
          }
      };
      /* GET JSON and Render to our API */
      http.get(http_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    }
  });

  app.get('/unis/idms/measurements', function(req, res) {
    // console.log('STATUS: ' + res.statusCode);
    // console.log('HEADERS: ' + JSON.stringify(res.headers));
    // console.log('BODY: ' + JSON.stringify(res.body));

    if (production) {
      console.log('running in production');

      /* HTTPS Options */
      var https_get_options = {
        hostname: idms_host,
        port: idms_port,
        key: fs.readFileSync(unis_key),
        cert: fs.readFileSync(unis_cert),
        requestCert: true,
        rejectUnauthorized: false,
        path: '/measurements?properties.geni.slice_uuid=' + slice_uuid,
        // path: '/measurements',
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      /* GET JSON and Render to our API */
      https.get(https_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    } else {
      /* HTTP Options */
      var http_get_options = {
          hostname: idms_host,
          port: idms_port,
          path: '/measurements',
          method: 'GET',
          headers: {
              'Content-type': 'application/perfsonar+json',
              'connection': 'keep-alive'
          }
      };
      /* GET JSON and Render to our API */
      http.get(http_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    }
  });

  app.get('/unis/idms/measurements/:id', function(req, res) {
    console.log("measurement id: " + req.params.id);
    // console.log('STATUS: ' + res.statusCode);
    // console.log('HEADERS: ' + JSON.stringify(res.headers));
    // console.log('BODY: ' + JSON.stringify(res.body));

    var measurement_id = req.params.id;

    if (production) {
      console.log('running in production');

      /* HTTPS Options */
      var https_get_options = {
        hostname: idms_host,
        port: idms_port,
        key: fs.readFileSync(unis_key),
        cert: fs.readFileSync(unis_cert),
        requestCert: true,
        rejectUnauthorized: false,
        path: '/measurements/' + measurement_id + '?properties.geni.slice_uuid=' + slice_uuid,
        // path: '/measurements/' + measurement_id,
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      /* GET JSON and Render to our API */
      https.get(https_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    } else {
      /* HTTP Options */
      var http_get_options = {
        hostname: idms_host,
        port: idms_port,
        path: '/measurements/' + measurement_id,
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      /* GET JSON and Render to our API */
      http.get(http_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    }
  });

  app.get('/unis/idms/metadata', function(req, res) {
    // console.log('STATUS: ' + res.statusCode);
    // console.log('HEADERS: ' + JSON.stringify(res.headers));
    // console.log('BODY: ' + JSON.stringify(res.body));

    if (production) {
      console.log('running in production');

      /* HTTPS Options */
      var https_get_options = {
        hostname: idms_host,
        port: idms_port,
        key: fs.readFileSync(unis_key),
        cert: fs.readFileSync(unis_cert),
        requestCert: true,
        rejectUnauthorized: false,
        path: '/metadata?parameters.geni.slice_uuid=' + slice_uuid,
        // path: '/metadata',
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      /* GET JSON and Render to our API */
      https.get(https_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    } else {
      /* HTTP Options */
      var http_get_options = {
          hostname: idms_host,
          port: idms_port,
          path: '/metadata',
          method: 'GET',
          headers: {
              'Content-type': 'application/perfsonar+json',
              'connection': 'keep-alive'
          }
      };
      /* GET JSON and Render to our API */
      http.get(http_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    }
  });

  app.get('/unis/idms/metadata/:id', function(req, res) {
    console.log("metadata id: " + req.params.id);
    // console.log('STATUS: ' + res.statusCode);
    // console.log('HEADERS: ' + JSON.stringify(res.headers));
    // console.log('BODY: ' + JSON.stringify(res.body));

    var metadata_id = req.params.id;

    if (production) {
      console.log('running in production');

      /* HTTPS Options */
      var https_get_options = {
        hostname: idms_host,
        port: idms_port,
        key: fs.readFileSync(unis_key),
        cert: fs.readFileSync(unis_cert),
        requestCert: true,
        rejectUnauthorized: false,
        path: '/metadata/' + metadata_id + '?parameters.geni.slice_uuid=' + slice_uuid,
        // path: '/metadata/' + metadata_id,
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      /* GET JSON and Render to our API */
      https.get(https_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    } else {
      /* HTTP Options */
      var http_get_options = {
        hostname: idms_host,
        port: idms_port,
        path: '/metadata/' + metadata_id,
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      /* GET JSON and Render to our API */
      http.get(http_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    }
  });

  app.get('/unis/idms/data', function(req, res) {
    // console.log('STATUS: ' + res.statusCode);
    // console.log('HEADERS: ' + JSON.stringify(res.headers));
    // console.log('BODY: ' + JSON.stringify(res.body));

    if (production) {
      console.log('running in production');

      // HTTPS Options
      var https_get_options = {
        hostname: idms_ms_host,
        port: idms_ms_port,
        key: fs.readFileSync(unis_key),
        cert: fs.readFileSync(unis_cert),
        requestCert: true,
        rejectUnauthorized: false,
        // path: '/data?properties.geni.slice_uuid=' + slice_uuid,
        path: '/data',
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      // GET JSON and Render to our API
      https.get(https_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    } else {
      // HTTP Options
      var http_get_options = {
          hostname: idms_ms_host,
          port: idms_ms_port,
          path: '/data',
          method: 'GET',
          headers: {
              'Content-type': 'application/perfsonar+json',
              'connection': 'keep-alive'
          }
      };
      // GET JSON and Render to our API
      http.get(http_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    }
  });

  app.get('/unis/idms/data/:id', function(req, res) {
    console.log("data id: " + req.params.id);
    // console.log('STATUS: ' + res.statusCode);
    // console.log('HEADERS: ' + JSON.stringify(res.headers));
    // console.log('BODY: ' + JSON.stringify(res.body));

    var data_id = req.params.id;

    if (production) {
      console.log('running in production');

      // HTTPS Options
      var https_get_options = {
        hostname: idms_ms_host,
        port: idms_ms_port,
        key: fs.readFileSync(unis_key),
        cert: fs.readFileSync(unis_cert),
        requestCert: true,
        rejectUnauthorized: false,
        // path: '/data/' + data_id + '?properties.geni.slice_uuid=' + slice_uuid,
        path: '/data/' + data_id,
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      // GET JSON and Render to our API
      https.get(https_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    } else {
      // HTTP Options
      var http_get_options = {
        hostname: idms_ms_host,
        port: idms_ms_port,
        path: '/data/' + data_id,
        method: 'GET',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'connection': 'keep-alive'
        }
      };
      // GET JSON and Render to our API
      http.get(http_get_options, function(http_res) {
        var data = '';

        http_res.on('data', function (chunk) {
          data += chunk;
        });
        http_res.on('end',function() {
          var obj = JSON.parse(data);
          // console.log( obj );
          res.json( obj );
        });
        http_res.on('error',function() {
          console.log('problem with request: ' + e.message);
          res.send( 404 );
        });
      });
    }
  });

  app.get('*', function(req, res) {
    res.sendfile('./public/index.html');
  });
 return self ;
};
