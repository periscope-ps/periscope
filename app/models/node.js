/*
 * Node Schema from UNIS
 * app/models/
 * node.js
 */

var mongoose = require('mongoose');

var NodeSchema = mongoose.Schema( {
    name: String,
    urn: String,
    ts: Number
});

module.exports = mongoose.model('Node', NodeSchema);