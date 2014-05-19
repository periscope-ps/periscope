/*
 * Server App
 * server.js
 */

/* Include Modules */
var express = require('express')
  , http = require('http')
//  , mongoose = require('mongoose')
  , database = require('./config/db');

/* Create App */
var app = express();

/* Database Connection */
//var db = mongoose.connection;

/* Check db connection */
/*db.on('error', console.error);
db.once('open', function() {
  console.log('Connected to ' + database.url)
});*/

/* Connect to db */
//mongoose.connect(database.url);

/* App Configuration */
app.configure(function() {
  app.set('port', process.env.PORT || 3000);
  app.use(express.static(__dirname + '/public'));
  app.use(express.favicon(__dirname + '/public/images/favicon.ico'));
  app.use(express.logger('dev'));
  app.use(express.bodyParser());
  app.use(express.methodOverride());
});

/* development only */
if ('development' == app.get('env')) {
  app.use(express.errorHandler());
}

/* All Server Routes */
require('./app/routes')(app);

/* Create HTTP Server and Listen on a Port */
http.createServer(app).listen(app.get('port'), function(){
  console.log('Node server lending an ear on port ' + app.get('port'));
});

/* Expose app */
exports = module.exports = app;
