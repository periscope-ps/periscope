/*
 * Service Schema from UNIS
 * app/models/
 * service.js
 */

var mongoose = require('mongoose');

var ServiceSchema = mongoose.Schema( {
    name: String,
    urn: String,
    ts: Number
});

module.exports = mongoose.model('Service', ServiceSchema);