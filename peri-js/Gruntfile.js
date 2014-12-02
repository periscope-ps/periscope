module.exports = function(grunt) {

    // Project configuration.
    grunt.initConfig({
	pkg: grunt.file.readJSON('package.json'),
	bower_concat: {
	    all: {
		dest: 'public/final.js',
		cssDest: 'public/final.css',
		exclude: [
		],
		dependencies: {
		},
		bowerOptions: {
		    relative: false
		}
	    }
	}
    });

    // Load the plugin that provides the concat task.
    grunt.loadNpmTasks('grunt-bower-concat');
    // Default task(s).
    grunt.registerTask('default', ['bower_concat']);
};
