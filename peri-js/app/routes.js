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

// production
var production = true;
var unis_host = 'unis.incntre.iu.edu';
var unis_port = '8443';
var unis_cert = '/usr/local/etc/certs/unis-proxy.pem';
var unis_key = '/usr/local/etc/certs/unis-proxy.pem';

// development
// var production = false;
// var unis_host = 'dev.incntre.iu.edu';
// var unis_host = 'localhost';
// var unis_port = '8888';
// var unis_port = '9001';

var slice_info = [];
var filePath = '/usr/local/etc/node.info';
var slice_uuid = '';
var os_name = '';
var distro = '';

module.exports = function(app) {

  var exec = require('child_process').exec;
  var child1, child2;

  child1 = exec('uname -s',
    function (error, stdout, stderr) {
      os_name = stdout;
      console.log('os_name: ' + os_name);
      if (error !== null) {
        console.log('exec error: ' + error);
      }
  });

  child2 = exec('head -1 /etc/issue',
    function (error, stdout, stderr) {
      distro = stdout;
      console.log('distro: ' + distro);
      if (error !== null) {
        console.log('exec error: ' + error);
      }
  });

  fs.readFile(filePath, {encoding: 'utf-8'}, function(err, data) {
    if (err) {
      console.log(err);
    } else {
      var fileData = data.toString().split('\n');
      var split, project, slice, gn, exAddy, ms, unis;

      for(line in fileData) {
        split = fileData[line].split('=');

        if(split[0] === 'external_address')
          exAddy = split[1];

        if (split[0] === 'gn_address')
          gn = split[1];

        if(split[0] === 'unis_instance')
          unis = split[1];

        if(split[0] === 'ms_instance')
          ms = split[1];

        if (split[0] === 'node_id') {
          project = split[2].split('+');
          slice = project[3].split(':');
        }

        if(split[0] === 'auth_uuid')
          slice_uuid = split[1];
      }
      slice_info.push({'external_address': exAddy, 'gn_address': gn, 'unis_instance': unis, 'ms_url': ms, 'project': project[1], 'slice': slice[0], 'slice_uuid': slice_uuid, 'os_name': os_name, 'distro': distro});
      console.log(slice_info);
    }
  });

  app.get('/api', function(req, res) {
    console.log('STATUS: ' + res.statusCode);
    console.log('HEADERS: ' + JSON.stringify(res.headers));
    console.log('BODY: ' + JSON.stringify(res.body));

    var routes = [];
    var hostname = req.headers.host;
    var pathname = url.parse(req.url).pathname;

    routes.push('http://' + hostname + pathname + '/slice');
    routes.push('http://' + hostname + pathname + '/nodes');
    routes.push('http://' + hostname + pathname + '/services');
    routes.push('http://' + hostname + pathname + '/measurements');
    routes.push('http://' + hostname + pathname + '/metadata');
    // routes.push('http://' + hostname + pathname + '/helm');
    // routes.push('http://' + hostname + pathname + '/help');

    res.json(routes);
  });

  app.get('/api/slice', function(req, res) {
    console.log('STATUS: ' + res.statusCode);
    console.log('HEADERS: ' + JSON.stringify(res.headers));
    console.log('BODY: ' + JSON.stringify(res.body));

    console.log(slice_info);
    res.json(slice_info);
  });

  app.get('/api/nodes', function(req, res) {
    console.log('STATUS: ' + res.statusCode);
    console.log('HEADERS: ' + JSON.stringify(res.headers));
    console.log('BODY: ' + JSON.stringify(res.body));

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
          console.log( obj );
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
          console.log( obj );
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

  app.get('/api/nodes/:id', function(req, res) {
    console.log("node id: " + req.params.id);
    console.log('STATUS: ' + res.statusCode);
    console.log('HEADERS: ' + JSON.stringify(res.headers));
    console.log('BODY: ' + JSON.stringify(res.body));

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
          console.log( obj );
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

  app.get('/api/services', function(req, res) {
    console.log('STATUS: ' + res.statusCode);
    console.log('HEADERS: ' + JSON.stringify(res.headers));
    console.log('BODY: ' + JSON.stringify(res.body));

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
          console.log( obj );
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
          console.log( obj );
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

  app.get('/api/services/:id', function(req, res) {
    console.log("service id: " + req.params.id);
    console.log('STATUS: ' + res.statusCode);
    console.log('HEADERS: ' + JSON.stringify(res.headers));
    console.log('BODY: ' + JSON.stringify(res.body));

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
          console.log( obj );
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

  app.get('/api/measurements', function(req, res) {
    console.log('STATUS: ' + res.statusCode);
    console.log('HEADERS: ' + JSON.stringify(res.headers));
    console.log('BODY: ' + JSON.stringify(res.body));

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
          console.log( obj );
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

  app.get('/api/measurements/:id', function(req, res) {
    console.log("measurement id: " + req.params.id);
    console.log('STATUS: ' + res.statusCode);
    console.log('HEADERS: ' + JSON.stringify(res.headers));
    console.log('BODY: ' + JSON.stringify(res.body));

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
          console.log( obj );
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

  app.post('/api/measurements', function(req, res) {
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
          console.log("return obj: " + JSON.stringify(obj));
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
          console.log("return obj: " + JSON.stringify(obj));
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

  app.put('/api/measurements/:id', function(req, res) {
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
          console.log("return obj: " + JSON.stringify(obj));
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
          console.log("return obj: " + JSON.stringify(obj));
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

  app.delete('/api/measurements/:id', function(req, res) {
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
          console.log("return obj: " + JSON.stringify(obj));
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
          console.log("return obj: " + JSON.stringify(obj));
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

  app.get('/api/metadata', function(req, res) {
    console.log('STATUS: ' + res.statusCode);
    console.log('HEADERS: ' + JSON.stringify(res.headers));
    console.log('BODY: ' + JSON.stringify(res.body));

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
        // path: '/metadata?properties.geni.slice_uuid=' + slice_uuid,
        path: '/metadata',
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
          console.log( obj );
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

  app.get('/api/data/:id', function(req, res) {
    console.log("data id: " + req.params.id);
    console.log('STATUS: ' + res.statusCode);
    console.log('HEADERS: ' + JSON.stringify(res.headers));
    console.log('BODY: ' + JSON.stringify(res.body));

    var data_id = req.params.id;

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
        // path: '/data/' + data_id + '?properties.geni.slice_uuid=' + slice_uuid,
        path: '/data/' + data_id,
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
          console.log( obj );
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
        path: '/data/' + data_id,
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

  /*app.get('/api/helm', function(req, res) {

    // HTTP Options
    var options = {
        hostname: 'localhost',
        port: 8888,
        path: '/measurements',
        method: 'GET',
        headers: {
            'content-type': 'application/json',
            'connection': 'keep-alive'
        }
    };

    // GET JSON and Render to our API
    http.get(options, function(http_res) {
      var data = '';

      http_res.on('data', function (chunk) {
        data += chunk;
      });

      http_res.on('end',function() {
        var obj = JSON.parse(data);
        console.log( obj );
        res.json( obj );
      });

    });

    // Manually invoke helm approach
    var filePath = '/Users/MarksMacMachine/research/UNISrt/samples/HELM/helm.conf';

    fs.readFile(filePath, {encoding: 'utf-8'}, function(err, data) {
      if (err) {
        console.log(err);
        res.send(err);
      } else {
        var conf = JSON.parse(data);
        console.log(conf);
        res.json(conf);
      }
    });
  });*/

  /*app.post('/api/helm', function(req, res) {
    // store result
    // var post_data = JSON.stringify(req.body);

    // Manually invoke helm approach
    var filePath = '/Users/MarksMacMachine/research/UNISrt/samples/HELM/helm.conf';

    console.log("post length: " + post_data.length);
    console.log("post data: " + post_data);

    fs.writeFile(filePath, post_data, function(err) {
      if(err) {
        console.log(err);
      } else {
        console.log("The file was saved!");
        var exec = require('child_process').exec;
        var child;

        child = exec('python /Users/MarksMacMachine/research/UNISrt/samples/HELM/helm.py',
          function (error, stdout, stderr) {
            console.log('stdout: ' + stdout);
            console.log('stderr: ' + stderr);
            if (error !== null) {
              console.log('exec error: ' + error);
            }
        });
      }
    });
  });*/

  /*app.get('/api/help', function(req, res) {
    console.log('STATUS: ' + res.statusCode);
    console.log('HEADERS: ' + JSON.stringify(res.headers));
    console.log('BODY: ' + JSON.stringify(res.body));

    var helpMe = [];

    helpMe.push('http://www.google.com');

    // render as json
    res.json(helpMe);

    // catch request error and render error page
    req.on('error', function(e) {
      console.log('problem with request: ' + e.message);
    });
  });*/

  app.get('*', function(req, res) {
    res.sendfile('./public/index.html');
  });

};
