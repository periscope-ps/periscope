/*
 * API and Browser Routes
 * app/
 * routes.js
 */

var Node = require('./models/node')
  , Service = require('./models/service')
  , fs = require('fs')
  , path = require('path');


module.exports = function(app) {  

  app.get('/slice', function(req, res) {     

    var store = [];
    var filePath = '/usr/local/etc/node.info';

    fs.readFile(filePath, {encoding: 'utf-8'}, function(err, data) {
      if (err) {
        console.log(err);
        res.send(err);
      } else {
        // console.log('received data: ' + data);
        
        var fileData = data.toString().split('\n');
        var split, project, slice, gn;

        for(line in fileData) {
          split = fileData[line].split('=');
          
          if (split[0] === 'gn_address')
            gn = split[1];

          if (split[0] === 'node_id') {
            project = split[2].split('+');
            slice = project[3].split(':');

            store.push({'gn_address': gn, 'project': project[1], 'slice': slice[0]});
          }
        }
      }
      console.log(store);
      res.json(store);
    });
  });

  app.get('/nodes', function(req, res) {
    
    Node.find(function(err, nodes) {

      if (err)
        res.send(err);

      console.log(nodes);
      res.json(nodes);
    });
  });

  app.get('/services', function(req, res) {
    
    Service.find(function(err, services) {

      if (err)
        res.send(err);

      console.log(services);
      res.json(services);
    });
  });

  app.get('*', function(req, res) {
    res.sendfile('./public/index.html');
  });

};