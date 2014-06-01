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
  , url = require('url');
  //, querystring = require('querystring');


module.exports = function(app) {

  app.get('/api', function(req, res) {
    var routes = [];
    var hostname = req.headers.host;
    var pathname = url.parse(req.url).pathname;

    routes.push('http://' + hostname + pathname + '/slice');
    routes.push('http://' + hostname + pathname + '/nodes');
    routes.push('http://' + hostname + pathname + '/services');
    routes.push('http://' + hostname + pathname + '/measurements');
    routes.push('http://' + hostname + pathname + '/helm');

    res.json(routes);
  });

  app.get('/api/slice', function(req, res) {

    var store = [];
    var filePath = '/usr/local/etc/node.info';

    fs.readFile(filePath, {encoding: 'utf-8'}, function(err, data) {
      if (err) {
        console.log(err);
        res.send(err);
      } else {
        console.log('received data: ' + data);

        var fileData = data.toString().split('\n');
        var split, project, slice, gn, exAddy, ms, uuid, unis;

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
            uuid = split[1];
        }
        store.push({'external_address': exAddy, 'gn_address': gn, 'unis_instance': unis, 'ms_url': ms, 'project': project[1], 'slice': slice[0], 'slice_uuid': uuid});
      }
      console.log(store);
      res.json(store);
    });
  });

  app.get('/api/nodes', function(req, res) {

    /* HTTP Options */
    var options = {
        hostname: 'localhost',
        port: 8888,
        path: '/nodes',
        method: 'GET',
        headers: {
            'content-type': 'application/json',
            'connection': 'keep-alive'
        }
    };

    /* GET JSON and Render to our API */
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

    /* Access Model Created from Mongo */
    /*Node.find(function(err, nodes) {

      if (err)
        res.send(err);

      console.log(nodes);
      res.json(nodes);
    });*/
  });

  app.get('/api/services', function(req, res) {

    /* HTTP Options */
    var options = {
        hostname: 'localhost',
        port: 8888,
        path: '/services',
        method: 'GET',
        headers: {
            'content-type': 'application/json',
            'connection': 'keep-alive'
        }
    };

    /* GET JSON and Render to our API */
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

    /* Access Model Created from Mongo */
    /*Service.find(function(err, services) {

      if (err)
        res.send(err);

      console.log(services);
      res.json(services);
    });*/
  });

  app.get('/api/measurements', function(req, res) {

    /* HTTP Options */
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

    /* GET JSON and Render to our API */
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

    /* Access Model Created from Mongo */
    /*Service.find(function(err, services) {

      if (err)
        res.send(err);

      console.log(services);
      res.json(services);
    });*/
  });

  app.post('/api/measurements', function(req, res) {
    // store result
    var post_data = JSON.stringify(req.body);

    console.log("post length: " + post_data.length);

    /* HTTP Options */
    var post_options = {
        hostname: 'localhost',
        port: 8888,
        path: '/measurements',
        method: 'POST',
        headers: {
            'Content-type': 'application/perfsonar+json',
            'Content-Length': post_data.length
        }
    };

    /* POST form measurement data to UNIS */
    var post_req = http.request(post_options, function(http_res) {
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
    });

    post_req.on('error', function(e) {
      console.log('problem with request: ' + e.message);
    });

    // write data to request body
    console.log("post_data: " + post_data);
    post_req.write(post_data);
    post_req.end();
  });

  app.get('/api/helm', function(req, res) {

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
  });

  app.post('/api/helm', function(req, res) {
    // store result
    var post_data = JSON.stringify(req.body);
    var filePath = '/Users/MarksMacMachine/research/UNISrt/samples/HELM/helm.conf';

    /*function run_cmd(cmd, args, callBack ) {

      var child = exec(cmd, args);
      var resp = "";

      child.stdout.on('data', function (buffer) { resp += buffer.toString() });
      child.stdout.on('end', function() { callBack (resp) });
    };*/

    console.log("post length: " + post_data.length);
    console.log("post data: " + post_data);

    fs.writeFile(filePath, post_data, function(err) {
      if(err) {
        console.log(err);
      } else {
        console.log("The file was saved!");
        var exec = require('child_process').exec;
        var child;

        // run_cmd( "cat /Users/MarksMacMachine/research/UNISrt/samples/HELM/helm.conf", [], function(text) { console.log ("command output: " + text) });
        // run_cmd( "python /Users/MarksMacMachine/research/UNISrt/samples/HELM/helm.py", [], function(text) { console.log ("command output: " + text) });
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
  });

  app.get('*', function(req, res) {
    res.sendfile('./public/index.html');
  });

};
