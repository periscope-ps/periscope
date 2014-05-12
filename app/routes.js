/*
 * API and Browser Routes
 * app/
 * routes.js
 */

var Node = require('./models/node');
var Service = require('./models/service');

module.exports = function(app) {

  app.get('/nodes', function(req, res) {
    
    Node.find(function(err, nodes) {

      if (err)
        res.send(err);

      res.json(nodes);
    });
  });

  app.get('/services', function(req, res) {
    
    Service.find(function(err, services) {

      if (err)
        res.send(err);

      res.json(services);
    });
  });

  app.get('*', function(req, res) {
    res.sendfile('./public/index.html');
  });

};