/*
 * Server App
 * server.js
 */

// include modules
var express = require('express')
  , http = require('http')
  , socketio = require('socket.io');
  // , mongoose = require('mongoose')
  // , database = require('./app/config/db');

// create app, server, sockets
var app = module.exports = express();
var server = http.createServer(app);
var io = socketio.listen(server);

// database connection
// var db = mongoose.connection;

// check db connection
// db.on('error', console.error);
// db.once('open', function() {
  // console.log('Connected to ' + database.url)
// });

// connect to db
// mongoose.connect(database.url);

// app configuration
app.configure(function() {
  app.set('port', process.env.PORT || 42424);
  app.use(express.static(__dirname + '/public'));
  app.use(express.favicon(__dirname + '/public/images/favicon.ico'));
  app.use(express.logger('dev'));
  app.use(express.json());
  app.use(express.urlencoded());
  app.use(express.methodOverride());
});

// configure enviroments
app.configure('development', function(){
  app.use(express.errorHandler({ dumpExceptions: true, showStack: true }));
});
app.configure('production', function(){
  app.use(express.errorHandler());
});

// restful api routes
require('./app/routes')(app);

// create http server and listen on a port */
server.listen(app.get('port'), function(){
  console.log('HTTP server on port ' + app.get('port') + ' - running as ' + app.settings.env);
});

// setup socket.io communication
io.sockets.on('connection', require('./app/sockets'));
