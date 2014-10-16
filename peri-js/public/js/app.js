/*
 * Setup Our Angular App
 * public/js/
 * app.js
 */

angular.module('measurementApp', [ 'ngRoute', 'ngAnimate', 'ui.utils',
		'ui.bootstrap', 'nvd3ChartDirectives', 'directedGraphModule',
		'appRoutes', 'SliceCtrl', 'SliceService', 'NodeCtrl', 'NodeService',
		'ServiceCtrl', 'ServiceService', 'BlippCtrl', 'BlippService',
		'MeasurementCtrl', 'MeasurementService', 'HelmCtrl', 'HelmService',
		'HelpCtrl', 'HelpService', 'MetadataCtrl', 'MetadataService',
		'IdmsMapCtrl', 'IdmsCtrl', 'IdmsService', 'PortService', 'SocketService',
		'schemaForm' ]);


